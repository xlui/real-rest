from flask import Flask, request, jsonify, current_app
from flask_script import Manager, Shell

from app import db
from app.models import User
from app.my_exception import MyException
from conf.config import Config

app = Flask(__name__)
app.config.from_object(Config)
manager = Manager(app)
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    json = [user.get_json() for user in users]
    return jsonify(json)


@app.route('/<user_id>', methods=['GET'])
def get_one(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify(user.get_json())
    else:
        raise MyException('user id is invalid!')


@app.route('/', methods=['POST'])
def post():
    if not request.json or not ('username' in request.json and 'password' in request.json):
        raise MyException('request payload must be JSON format and ALL field off entity `user` should be included!')
    user = User.query.get(request.json.get('username'))
    if user:
        raise MyException('username already exist!')
    else:
        user = User(username=request.json.get('username'),
                    password=request.json.get('password'))
        db.session.add(user)
        db.session.commit()
        return jsonify(user.get_json())


@app.route('/<user_id>', methods=['PUT'])
def put(user_id):
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        raise MyException('request payload must be JSON format and all field off entity `user` should be included!')
    user = User.query.get(user_id)
    if user:
        user.username = request.json.get('username')
        user.password = request.json.get('password')
        return jsonify(user.get_json())
    else:
        raise MyException('user id is invalid!')


@app.route('/<user_id>', methods=['PATCH'])
def patch(user_id):
    if not request.json:
        raise MyException('request payload must be JSON format!')
    user = User.query.get(user_id)
    if user:
        # check username or password is contained or not
        username = request.json.get('username')
        password = request.json.get('password')
        if not username and not password:
            raise MyException('At least include one field off entity `user`!')

        if username:
            user.username = username
        if password:
            user.password = password
        return jsonify(user.get_json())
    else:
        print('User id is invalid!')
        raise MyException('user id is invalid!', 400)


@app.route('/<user_id>', methods=['DELETE'])
def delete(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        return jsonify({
            'message': 'Successfully delete user {id}'.format(id=user_id)
        })
    else:
        raise MyException('user id is invalid!')


@app.route('/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json:
        raise MyException('request body must be in JSON format!')
    user = User.query.get(request.json.get('username'))  # type: User
    if not user:
        raise MyException('Username is invalid!')
    if user.password == request.json.get('password'):
        return jsonify({
            'login': 'Success!',
            'token': user.generate_token().decode('utf-8')
        })
    else:
        raise MyException('Password is incorrect!')


@app.route('/verify', methods=['GET'])
def verify():
    token = request.headers.get('authorization')
    if not token:
        raise MyException('Must include token in request header!')
    user = User.verify_token(token)  # type: User
    if user:
        return jsonify({
            'verify': 'Success',
            'user': user.username
        })
    else:
        raise MyException('Token is invalid!')


@app.errorhandler(MyException)
def handle_my_exception(error: MyException):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    def make_shell_context():
        return dict(User=User, app=current_app, db=db)
    manager.add_command('shell', Shell(make_context=make_shell_context))
    manager.run()
