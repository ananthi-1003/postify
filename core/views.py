from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Post.objects.create(user=request.user, text=content)
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
    return render(request, 'profile.html')

@login_required
def friends(request):
    return render(request, 'friends.html')

@login_required
def edit_profile(request):
    return redirect('profile')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('feed')
