from conf.config import Config
from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String(128))

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }

    def generate_token(self, expiration=3600):
        # default expiration time: 1 hour
        serializer = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return serializer.dumps({
            'username': self.username
        })

    @staticmethod
    def verify_token(token):
        serializer = Serializer(Config.SECRET_KEY)
        try:
            data = serializer.loads(token) # type: dict
            return User.query.get(data.get('username'))
        except Exception as e:
            print(e)
            return None

    def __repr__(self) -> str:
        return 'User(username=%r, password=%r)' % (self.username, self.password)

    def __str__(self) -> str:
        return '<User %r>' % self.username
