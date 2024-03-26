from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from .models import Post

import re

# Get the User model
User_Model = get_user_model()


def SignUp(request):
    """
    User sign up view.
    """
    if request.method == "POST":
        First_Name = request.POST.get("First_Name")
        Last_Name = request.POST.get("Last_Name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validate email format
        if not validate_email_format(email):
            messages.error(request, "Please provide a valid email address with the domain 'gmail.com'.")
            return render(request, "SignUp.html", {
                "First_Name": First_Name,
                "Last_Name": Last_Name,
                "username": username,
                "email": email,
                "phone_number": phone_number,
            })

        # Validate phone number format
        if not validate_phone_number(phone_number):
            messages.error(request, "The format of the phone number is incorrect.")
            return render(request, "SignUp.html", {
                "First_Name": First_Name,
                "Last_Name": Last_Name,
                "username": username,
                "email": email,
                "phone_number": phone_number,
            })

        if password != confirm_password:
            messages.error(request, "Passwords must match for confirmation.")
        elif not password_security_checker(password):
            messages.error(request, "Please choose a secure password")
        elif User_Model.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif User_Model.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User_Model.objects.create_user(
                first_name=First_Name,
                last_name=Last_Name,
                username=username,
                email=email,
                password=password,
            )
            if user is not None:
                messages.success(request, 'Welcome! Your account has been successfully created.')
                return redirect("SignIn")
            else:
                messages.error(request, "Try again!")
                return render(request, "SignUp.html", {
                    "First_Name": First_Name,
                    "Last_Name": Last_Name,
                    "username": username,
                    "email": email,
                })

    else:
        return render(request, "SignUp.html")


def validate_email_format(email):
    """
    Validate email format.
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return bool(re.match(pattern, email))


def validate_phone_number(phone_number):
    """
    Validate phone number format.
    """
    pattern = r'^\+[0-9]+$'
    return bool(re.match(pattern, phone_number))


def password_security_checker(password):
    """
    Check password strength.
    """
    if len(password) < 8:
        return False
    if not (re.search(r"[a-z]", password) and re.search(r"[A-Z]", password)):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True


@login_required(login_url="SignIn")
def LogOut(request):
    """
    Logout User.
    """
    logout(request)
    return redirect("SignIn")


def SignIn(request):
    """
    User sign in view.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("List_of_Posts")
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "SignIn.html",
                          {"username": username})
    else:
        return render(request, "SignIn.html")


def profile(request, esport):
    """
    User profile view.
    """
    profile = get_object_or_404(User_Model, esport=esport)
    return render(request, "profile.html", {"profile": profile})


@login_required(login_url="SignIn")
def View_Settings(request):
    """
    User settings view.
    """
    profile = request.user

    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        bio = request.POST.get("bio", "")

        profile.first_name = first_name
        profile.last_name = last_name
        profile.bio = bio

        if "profile_picture" in request.FILES:
            profile_picture = request.FILES["profile_picture"]
            profile.profile_picture = profile_picture

        profile.save()

        return redirect("profile", profile.esport)

    return render(request, "view_settings.html", {"profile": profile})


@login_required(login_url='SignIn')
def Created_Post(request):
    """
    Create a new post.
    """
    if request.method == 'POST':
        author = request.user
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title and content:
            post = Post.objects.create(author=author, title=title,
                                       content=content)
            messages.success(request, 'Post created!')
            return redirect('Post_Details', esport=post.esport)
        else:
            messages.error(request, 'Title and content fields cannot be empty.')
    return render(request, 'form.html')


def Post_Details(request, esport):
    """
    View post detail.
    """
    post = get_object_or_404(Post, esport=esport)
    if request.user.is_authenticated:
        post.views += 1
        post.save()
    return render(request, 'details.html', {'post': post})


@login_required(login_url='SignIn')
def Updated_Post(request, esport):
    """
    Update a post.
    """
    post = get_object_or_404(Post, esport=esport)
    if request.User != post.author:
        messages.error(request, "Editing privileges denied: You're not authorized to modify this post.")
        return redirect('Post_Details', esport=esport)

    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, 'Post updated!')
            return redirect('Post_Details', esport=post.esport)
        else:
            messages.error(request, 'Please provide both title and content.')

    return render(request, 'form.html', {'post': post})


@login_required(login_url='SignIn')
def Deleted_Post(request, esport):
    """
    Delete a post.
    """
    post = get_object_or_404(Post, esport=esport)
    if request.User != post.author:
        messages.error(request, "Editing privileges denied: You're not authorized to delete this post.")
        return redirect('Post_Details', esport=esport)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted!')
        return redirect('List_of_Posts')

    return render(request, 'deleted.html', {'post': post})


def List_of_Posts(request):
    """
    List all posts.
    """
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts': posts})
