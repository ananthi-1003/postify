from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        text = request.POST.get('content')
        if text:
            Post.objects.create(user=request.user, text=text)
    return redirect('feed')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'posts': posts})

@login_required
def friends(request):
    return render(request, 'friends.html')