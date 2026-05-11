from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Post, Like, Comment, Profile
from .forms import CommentForm, ProfileUpdateForm

@login_required
def home(request):
    if request.method == 'POST' and 'content' in request.POST:
        content = request.POST.get('content')
        if content:
            Post.objects.create(author=request.user, content=content)
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    
    posts = Post.objects.all().order_by('-created_at')
    comment_form = CommentForm()
    
    for post in posts:
        post.is_liked = Like.objects.filter(user=request.user, post=post).exists()
        post.comments = Comment.objects.filter(post=post).order_by('created_at')
    
    return render(request, 'home.html', {'posts': posts, 'comment_form': comment_form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created! Welcome to Postify')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    return redirect('home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('home')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added!')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'p_form': p_form, 'user_posts': user_posts})

def custom_404(request, exception):
    return render(request, '404.html', status=404)