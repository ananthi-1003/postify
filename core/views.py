from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile  # IDHU MUKKIYAM
from .models import Post     # Home page ku venum
from .forms import PostForm  # Nee create panna form

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                # 1. User ah save pannu
                user = form.save()
                
                # 2. Profile create pannu - Idhu illana 500 error varum
                Profile.objects.create(user=user)
                
                # 3. Auto login pannu
                login(request, user)
                return redirect('home')  # 'home' url name irukanum
            except Exception as e:
                # Error vandha signup page ku thiruppi anuppu
                form.add_error(None, f"Error: {e}")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts, 'form': form})