from django.db import models

# Create your models here.
# Yeah bro pls change all the field inside there, this is just an example to test out xd
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username