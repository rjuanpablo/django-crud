from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks_completed.html', {'tasks': tasks})

@login_required
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

@login_required    
def task_detail(request, task_id):
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            #if form.is_valid():
            form.save()
            return redirect('tasks')
            #else:
            return render(request, 'task_detail.html', {'task': task, 'form': form})
        except Exception:
            return render(request, 'task_detail.html', {'task': task,'form': form, 'error': 'An error occurred while updating the task.'})
    else:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})

@login_required
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
    
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
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