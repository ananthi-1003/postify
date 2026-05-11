from django.shortcuts import render
from .models import Post

def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts})

def profile(request):
    return render(request, 'profile.html')

def friends(request):
    return render(request, 'friends.html')