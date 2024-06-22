from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm(),
        })
    else:
        if request.POST['password1'] == request.POST['password2'] and request.POST['password1']!= '' and request.POST['username']!= '':
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return HttpResponse('successful signup! You can now log in.')
            except:
                return HttpResponse('Signup failed! Username already exists.')
            
        return HttpResponse('Signup failed! Passwords do not match or username is empty.')
    
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')