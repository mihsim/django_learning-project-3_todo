# redirect is used after new user has been created and logged in to direct him to new page
from django.shortcuts import render, redirect, get_object_or_404

# Form by django to put in username and password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# User model
from django.contrib.auth.models import User

# IntegrityError happens when you try to create a new username, but this name already is in database
from django.db import IntegrityError

# To automatically log in after user has been created
from django.contrib.auth import login, logout, authenticate

from django.utils import timezone


from .forms import TodoForm
from .models import Todo


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
                return redirect('current_todos')
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
        return redirect('current_todos')


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


def current_todos(request):
    todos = Todo.objects.filter(user=request.user, completed_time__isnull=True)
    return render(request, "todo/current_todos.html", {'todos': todos})


def create_todo(request):
    if request.method == "GET":
        return render(request, "todo/create_todo.html", {'form': TodoForm})
    else:
        try:
            # request.method == "POST"
            form = TodoForm(request.POST)
            # Form is missing user info so we can not save it to database yet (commit=False)
            # Rather we create a form object and save it to 'new_form'
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            # Now save it to db.
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, "todo/create_todo.html", {'form': TodoForm, "error": "Bad data provided by user. Try harder!"})


def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "GET":
        form = TodoForm(instance=todo)
        return render(request, "todo/view_todo.html", {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect("current_todos")
        except ValueError:
            return render(request, "todo/view_todo.html", {'todo': todo, 'form': form, 'error': "Bad data, please try harder."})


def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.completed_time = timezone.now()
        todo.save()
        return redirect("current_todos")


def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect("current_todos")
