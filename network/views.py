from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post

def index(request):

	if request.method == 'POST':

		if not request.user.is_authenticated:
			return redirect('index')

		content = request.POST['new_post_content']
		Post.objects.create(owner = request.user, content = content)

	posts = Post.objects.all().order_by('-created_date')
	return render(request, "network/pages/index.html", {'posts': posts})

def user_profile_view(request, username):

	user = None
	
	try:
		user = User.objects.get(username=username)	
	except User.DoesNotExist:
		return render(request, "network/pages/404.html")
	
	number_of_followers = user.get_number_of_followers()
	number_of_following = user.get_number_of_following()
	user_posts = user.posts.all().order_by('-created_date')

	return render(request, "network/pages/user_profile.html", {
		'user': user,
		'number_of_followers': number_of_followers,
		'number_of_following': number_of_following,
		'posts': user_posts
	})
# AUTH
def login_view(request):
	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "network/pages/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "network/pages/login.html")


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))


def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "network/pages/register.html", {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "network/pages/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "network/pages/register.html")
# END AUTH