from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Follow, Like, Post, User


class User_edit(forms.Form):
    image = forms.ImageField(required=False)
    header = forms.ImageField(required=False)
    first_name = forms.CharField(widget=forms.TextInput, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 1,'cols': 120, 'rows':8}), required=False)


def index(request):
    posts = Post.objects.all().order_by('-posted_date')
    p = Paginator(posts, 10)
    pnumber = request.GET.get('page')
    obj = p.get_page(pnumber)

    liked_post_id_list = likedPostList(request)

    return render(request, "network/index.html", {
        "posts": obj,
        "liked_post_id_list": liked_post_id_list
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


def new_post(request):
    if request.method == "POST":
        user = request.user
        post_content = request.POST["post-content"]

        add_post = Post.objects.create(user=user, content=post_content)

    return HttpResponseRedirect(reverse("index"))


def profile(request, username):
    user = User.objects.get(username=username)
    following_id_list = [] 
    
    try:
        follow = Follow.objects.get(user=user)
    except:
        follow = 0
    if Follow.objects.filter(user=request.user):
        for i in range(0, Follow.objects.get(user=request.user).following.count()):
            following_id_list.append(Follow.objects.get(user=request.user).following.values_list()[i][0])

    return render(request, "network/profile.html", {
        "user_profile": user,
        "follow": follow,
        "following_list": following_id_list,
        "posts": Post.objects.filter(user=user)
        })


def edit_user(request, username):
    get_user = User.objects.get(username=username) 

    if request.method == 'POST':
        form = User_edit(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=username)
            user.profile_photo = form.cleaned_data['image']
            user.header_photo = form.cleaned_data['header']
            user.first_name = form.cleaned_data['first_name']
            user.bio = form.cleaned_data['bio']
            user.save()

    return render(request, "network/edit_user.html", {
        "user": User.objects.get(username=username),
        "edit": User_edit(initial={"bio": get_user.bio, "first_name": get_user.first_name})    
    })


def edit(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        new_content = request.POST["edit-post"]
        print(new_content)
        post.content = new_content
        post.save()

    return HttpResponseRedirect(reverse("index"))


def following(request):
    following = Follow.objects.get(user=request.user).following.values_list()
    posts_list = [] 
    
    for follow in following:
        username = follow[4]
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user).order_by('-posted_date')
        posts_list.append(posts)
        
    p = Paginator(posts, 10)
    pnumber = request.GET.get('page')
    obj = p.get_page(pnumber)

    return render(request, "network/index.html", {
        "posts": obj
    })


def follow(request, username):
    user = User.objects.get(username=request.user.username)
    user_to_follow = User.objects.get(username=username)

    # make the user follow
    try:
        follow = Follow.objects.get(user=user)
        follow.following.add(user_to_follow)
    except:    
        follow = Follow.objects.create(user=user)
        follow.following.add(user_to_follow)

    # make the user to follow be followed
    try:
        user_to_follow = Follow.objects.get(user=user_to_follow)
        user_to_follow.followers.add(user)
    except:
        follow = Follow.objects.create(user=user_to_follow)
        follow.followers.add(user)

    url = reverse('profile', kwargs={'username': username})
    return HttpResponseRedirect(url)


def unfollow(request, username):
    user = User.objects.get(username=request.user.username)
    user_to_unfollow = User.objects.get(username=username)

    # make the user be unfollowed
    Follow.objects.get(user=user).following.remove(user_to_unfollow)
    Follow.objects.get(user=user_to_unfollow).followers.remove(user)

    url = reverse('profile', kwargs={'username': username})
    return HttpResponseRedirect(url)


def like(request, post, user):
    post_to_like = Post.objects.get(pk=post)
    user_that_likes = User.objects.get(username=user)
    
    # Create new like object if it doesn't exist
    if Like.objects.filter(post=post):
        like_post = Like.objects.get(post=post)
        like_post.user.add(user_that_likes)
        like_post.save()
    else:
        like_post = Like(post=post)
        like_post.save()
        like_post.user.add(user_that_likes)

    # Get list of all likes
    all_likes = Like.objects.get(post=post)
    all_likes_list = list(all_likes.user.all())

    # Determine the number of likes from the length of the list
    post_to_like.likes = len(all_likes_list)
    post_to_like.save()

    return redirect(request.META['HTTP_REFERER'])

def unlike(request, post, user):
    post_to_unlike = Post.objects.get(pk=post)
    user_that_unlikes = User.objects.get(username=user)

    # Remove user from user list of Like object corresponding to post id
    unlike_post = Like.objects.get(post=post)
    unlike_post.user.remove(user_that_unlikes)
    unlike_post.save()

    # Get list of all likes
    all_likes = Like.objects.get(post=post)
    all_likes_list = list(all_likes.user.all())

    # Determine the number of likes from the length of the list
    post_to_unlike.likes = len(all_likes_list)
    post_to_unlike.save()

    return redirect(request.META['HTTP_REFERER'])


def likedPostList(request):
    liked_post_id_list = []

    if request.user:
        liked_posts = Like.objects.filter(user=request.user).all()
        for post in liked_posts:
            liked_post_id_list.append(post.post)
    
    return liked_post_id_list