from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Task
from .forms import TaskForm

# Create your views here.


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
        })
    else:
        if request.POST['password1'] == request.POST['password2'] and request.POST['password1'] != '' and request.POST['username'] != '':
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'Username already exists.',
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            'error': 'Passwords do not match.',
        })


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')

def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except Exception:
            return render(request, 'create_task.html', {
                'form': TaskForm(),
                'error': 'An error occurred while creating the task.',
            })
    else:
        return render(request, 'create_task.html', {
            'form': TaskForm(),
        })
    
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})

def create_task_(request):
    if request.method == 'POST':
        print(request.POST)  # for debugging purposes, remove in production
        title = request.POST['title']
        description = request.POST['description']
        if 'important' in request.POST:  # check if 'important' checkbox is checked in the
            important = True
        else:
            important = False
        user = request.user
        Task.objects.create(title=title, description=description, important=important, user=user)
        return redirect('tasks')
    else:
        return render(request, 'create_task.html', {
            'form': TaskForm(),
        })

def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm(),
        })
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'Invalid username or password.',
            })


def signin2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'signin.html', {
                'error': 'Invalid username or password.',
            })
    else:
        return render(request, 'signin.html')