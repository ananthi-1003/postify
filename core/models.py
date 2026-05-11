from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    saves = models.ManyToManyField(User, related_name='saved_posts', blank=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}'
    
    def total_likes(self):
        return self.likes.count()
    
    def total_saves(self):
        return self.saves.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)

class Repost(models.Model):
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    theme = models.CharField(max_length=20, default='dark', choices=[('dark', 'Dark'), ('light', 'Light'), ('purple', 'Purple')])

    def __str__(self):
        return f'{self.user.username} Profile'