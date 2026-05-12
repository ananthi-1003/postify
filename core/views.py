from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post, Profile, Follow, Comment

@login_required
def home(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            Post.objects.create(user=request.user, content=content, image=image)
            return redirect('home')
    
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'posts': posts})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    followers_count = user.followers.count()
    following_count = user.following.count()
    
    context = {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'core/profile.html', context)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=username)

@login_required
def friends_list(request):
    following = User.objects.filter(followers__follower=request.user)
    followers = User.objects.filter(following__following=request.user)
    context = {'following': following, 'followers': followers}
    return render(request, 'core/friends.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect('home')

@login_required
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)
        saved = False
    else:
        post.saves.add(request.user)
        saved = True
    return JsonResponse({'saved': saved})

@login_required
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Post.objects.create(user=request.user, content=f"Shared: {post.content}", image=post.image)
    return redirect('home')

@login_required
def repost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Post.objects.create(user=request.user, content=post.content, image=post.image)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})