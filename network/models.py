from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime


class User(AbstractUser):
	
	avatar_img = models.URLField()
	following = models.ManyToManyField('self', related_name='followers', blank=True, symmetrical=False)
	
	def get_number_of_followers(self):
		return self.followers.count()

	def get_number_of_following(self):
		return self.following.count()


class Post(models.Model):

	owner = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
	content = models.CharField(max_length=200, blank=False, null=False)
	created_date = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(default=0)





