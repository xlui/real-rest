import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db = os.path.join(os.path.split(base_dir)[0], 'dev.sqlite')


class Config:
    # SQLALCHEMY
    SECRET_KEY = 'This is a secret key and should never export to the internet'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db
