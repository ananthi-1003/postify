from django import forms
from .models import Comment, Profile

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add a comment...', 'class': 'w-full p-2 rounded-lg bg-gray-700 border-gray-600'}))
    
    class Meta:
        model = Comment
        fields = ['content']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']