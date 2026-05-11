from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('profile/', views.profile, name='profile'),
    path('friends/', views.friends, name='friends'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('create-post/', views.create_post, name='create-post'),
]