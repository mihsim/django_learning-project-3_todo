# redirect is used after new user has been created and logged in to direct him to new page
from django.shortcuts import render, redirect

# Form by django to put in username and password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# User model
from django.contrib.auth.models import User

# IntegrityError happens when you try to create a new username, but this name already is in database
from django.db import IntegrityError

# To automatically log in after user has been created
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == "GET":
        # Display page
        return render(request, "todo/signupuser.html", {'form': UserCreationForm()})
    else:
        # Create new user
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST["password1"])
                # Save user to database
                user.save()
                # Log this user in
                login(request, user)
                # Send him to next page
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, "todo/signupuser.html", {'form': UserCreationForm(),
                                                                'error': "This username has already been taken. Please select another."})
        else:
            # Tell user that passwords did not match!
            return render(request, "todo/signupuser.html", {'form': UserCreationForm(),
                                                            'error': "Passwords did not match"})


def loginuser(request):
    if request.method == "GET":
        return render(request, "todo/loginuser.html", {'form': AuthenticationForm()})
    else:
        # authenticate returns a User object
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # If matching user was not found the value is None
        if user is None:
            return render(request, "todo/loginuser.html", {'form': AuthenticationForm(), 'error': 'Username and password did not match.'})
        login(request, user)
        return redirect('currenttodos')

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


def currenttodos(request):
    return render(request, "todo/currenttodos.html")
