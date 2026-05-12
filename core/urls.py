from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('friends/', views.friends, name='friends'),
    path('profile/<str:username>/', views.profile, name='profile'),
    
    # FOLLOW/UNFOLLOW - IDHU PUDHUSA
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    
    # LIKE, COMMENT, REPOST, SAVE
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('save/<int:post_id>/', views.save_post, name='save_post'),
    path('repost/<int:post_id>/', views.repost, name='repost'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
]