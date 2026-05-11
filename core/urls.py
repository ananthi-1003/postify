from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('save/<int:pk>/', views.save_post, name='save_post'),
    path('comment/<int:pk>/', views.comment_post, name='comment_post'),
    path('repost/<int:pk>/', views.repost, name='repost'),
    path('theme/', views.change_theme, name='change_theme'),
]