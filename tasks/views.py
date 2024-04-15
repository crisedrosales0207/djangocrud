from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Tasks
from .forms import TaskForm


# ? Create your views here.

# * Home View


def home(request):
    return render(request, 'home.html')

# * Signup View


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                print(user)
                login(request, user)
                return redirect('get_tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'err_message': 'User Already Exist'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'err_message': 'Password do not match'
            })


# * Login
def signin(request):
    if (request.method == 'GET'):
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        print(user)
        if (user is None):
            return render(request, 'login.html', {
                'form': AuthenticationForm, 'err_message': 'User or password not match'
            })
        else:
            login(request, user)
            return redirect('get_tasks')

# * LogOut


def signOut(request):
    logout(request)
    return redirect('home')


# * Create Tasks

def create_tasks(request):
    if (request.method == 'GET'):
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        form = TaskForm(request.POST)
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect ('get_tasks')


# * Tasks Pending
def get_tasks(request):
    tasks = Tasks.objects.filter(user=request.user, completed_at__isnull=True)
    print(tasks)
    return render(request, 'tasks.html', {'tasks': tasks})
