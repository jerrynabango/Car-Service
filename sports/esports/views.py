from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from .models import Post

import re

# Create your views here.
CustomUser = get_user_model()


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email_input = request.POST.get("email_input")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif not check_password_strength(password):
            messages.error(request, "Password is not strong enough")
        elif CustomUser.objects.filter(email=email_input).exists():
            messages.error(request, "Email Taken")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username Taken")
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email_input,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            if user is not None:
                messages.success(request, 'Welcome! Your account has been successfully created.')
                return redirect("signin")
            else:
                messages.error(
                    request, "Try again!."
                )

        return render(
            request,
            "registrations/signup.html",
            {
                "username": username,
                "email_input": email_input,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
    else:
        return render(request, "registrations/signup.html")


def check_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True


@login_required(login_url="signin")
def logout_user(request):
    logout(request)
    return redirect("signin")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("post_list")
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "registrations/signin.html",
                          {"username": username})
    else:
        return render(request, "registrations/signin.html")


def profile(request, esport):
    user_profile = get_object_or_404(CustomUser, esport=esport)
    return render(request, "profile.html", {"user_profile": user_profile})


@login_required(login_url="signin")
def settings(request):
    user_profile = request.user

    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        bio = request.POST.get("bio", "")

        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.bio = bio

        if "profile_picture" in request.FILES:
            profile_picture = request.FILES["profile_picture"]
            user_profile.profile_picture = profile_picture

        user_profile.save()

        return redirect("profile", user_profile.esport)

    return render(request, "settings.html", {"user_profile": user_profile})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, esport):
    post = get_object_or_404(Post, esport=esport)
    if request.user.is_authenticated:
        post.views += 1
        post.save()
    return render(request, 'post_detail.html', {'post': post})


@login_required(login_url='signin')
def post_create(request):
    if request.method == 'POST':
        author = request.user
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title and content:
            post = Post.objects.create(author=author, title=title,
                                       content=content)
            messages.success(request, 'Post created!')
            return redirect('post_detail', esport=post.esport)
        else:
            messages.error(request, 'Title and content fields cannot be empty.')
    return render(request, 'post_form.html')


@login_required(login_url='signin')
def post_update(request, esport):
    post = get_object_or_404(Post, esport=esport)
    if request.user != post.author:
        messages.error(request, "Editing privileges denied: You're not authorized to modify this post.")
        return redirect('post_detail', esport=esport)

    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, 'Post updated!')
            return redirect('post_detail', esport=post.esport)
        else:
            messages.error(request, 'Please provide both title and content.')

    return render(request, 'post_form.html', {'post': post})


@login_required(login_url='signin')
def post_delete(request, esport):
    post = get_object_or_404(Post, esport=esport)
    if request.user != post.author:
        messages.error(request, "Editing privileges denied: You're not authorized to delete this post.")
        return redirect('post_detail', esport=esport)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted!')
        return redirect('post_list')

    return render(request, 'post_confirm_delete.html', {'post': post})
