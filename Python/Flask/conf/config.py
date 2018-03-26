import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db = os.path.join(os.path.split(base_dir)[0], 'dev.sqlite')


class Config:
    # SQLALCHEMY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db
