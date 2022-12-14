from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from .models import User, Post
from .forms import PostForm


def index(request, posts=None):
    if posts: pass
    else: posts = Post.get_posts(type='ALL')

    items_per_page = 3
    pages = Paginator(posts, items_per_page)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)

    return render(request, "network/index.html", {
        'form': PostForm(),
        'page_obj': page_obj,
    })

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# It would be nice to transform this into a JScript that pops up the form,
# then saves the post, finally, queries the post and puts it at the top of the page
@login_required(login_url='login')
def create_post(request):
    # take request
    if (request.method == 'POST'):
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post_form.instance.poster = request.user
            post_form.save()
            return HttpResponseRedirect(reverse(index))

        return HttpResponse('Form was invalid')


def profile_page(request, username):
    # Make sure requested user exist
    try:
        requested_user = User.objects.get(username=username)
    except User.DoesNotExist:
        # This should be a cute page
        return HttpResponse(f'404 User {username} not found')
    posts = Post.get_posts(type='USER', user=requested_user)

    # Define follow message and wheter or not follow button
    user = request.user
    if (user == requested_user or not user.is_authenticated): follow_button = False
    else:
        if requested_user in user.following.all(): follow_button = 'Unfollow'
        else: follow_button = 'Follow'
    
    # Divide in pages
    items_per_page = 2
    pages = Paginator(posts, items_per_page)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)

    # This page should reuse a substructure of index, not include a completely new template.
    # It could be done with REACT
    return render(request, "network/profile_page.html", {
        'requested_user': requested_user,
        'page_obj': page_obj,
        'follow_button': follow_button,
    })


@login_required(login_url='login')
def following(request):
    posts = Post.get_posts('FOLLOWING', user=request.user)
    return index(request,posts)

@login_required(login_url='login')
def toggle_follow(request, followed_username, button_state):
    # Make sure followed exist
    try:
        followed_user = User.objects.get(username=followed_username)
    except User.DoesNotExist:
        # This should be a cute page
        return HttpResponse(f'404 User {followed_username} not found')

    if button_state == 'Follow':
        request.user.follow(followed_user)
    if button_state == 'Unfollow':
        request.user.unfollow(followed_user)

    return HttpResponseRedirect(reverse("profile_page", args=(followed_username,)))
