from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Comment, Repost, Profile
from .forms import PostForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user) # ← 500 Error fix
            login(request, user)
            messages.success(request, 'Account created! Welcome Ananthi 💙')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'home.html', {'posts': posts, 'form': form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

@login_required
def save_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.saves.all():
        post.saves.remove(request.user)
        saved = False
    else:
        post.saves.add(request.user)
        saved = True
    return JsonResponse({'saved': saved, 'total_saves': post.total_saves()})

@login_required
def comment_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, user=request.user, text=text)
    return redirect('home')

@login_required
def repost(request, pk):
    original = get_object_or_404(Post, id=pk)
    Repost.objects.create(original_post=original, user=request.user)
    messages.success(request, 'Reposted!')
    return redirect('home')

@login_required
def change_theme(request):
    if request.method == 'POST':
        theme = request.POST.get('theme')
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.theme = theme
        profile.save()
    return redirect('home')