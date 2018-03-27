from django.db import models


# Model entity
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
        }

    def __str__(self):
        return '{username}, {password}'.format(username=self.username, password=self.password)
