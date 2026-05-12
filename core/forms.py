from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': "What's happening?",
            'rows': 3,
            'style': 'background:#1a1025;border:1px solid #4c1d95;color:#f3e8ff;'
        }),
        label=''
    )
    
    class Meta:
        model = Post
        fields = ['content', 'image']

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Post your reply'}),
        label=''
    )
    
    class Meta:
        model = Comment
        fields = ['text']