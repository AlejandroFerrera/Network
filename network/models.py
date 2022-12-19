from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    avatar_img = models.URLField()
    following = models.ManyToManyField('self', related_name='followers')
