import os
from django.db import models                          # type: ignore

def unique_table_name():
    random_number = str(int(os.urandom(5).hex(), 16))[:10]
    return f"table_{random_number}"

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username

class FileUpload(models.Model):
    table_name = models.CharField(max_length=30, default=unique_table_name)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.table_name

#############################################################

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  #, default='default_password')
    # Add other fields if necessary

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
