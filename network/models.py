from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    avatar_img = models.URLField()
    following = models.ManyToManyField('self', related_name='followers')

class Post(models.Model):

    owner = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    content = models.CharField(max_length=200, blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)


