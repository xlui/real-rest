from . import db


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

    def __repr__(self) -> str:
        return 'User(username=%r, password=%r)' % (self.username, self.password)

    def __str__(self) -> str:
        return '<User %r>' % self.username
