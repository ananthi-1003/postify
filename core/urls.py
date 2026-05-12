from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # PROFILE + FOLLOW
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('follow/<str:username>/', views.follow_user, name='follow'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow'),
    path('friends/', views.friends_list, name='friends'),
    
    # LIKE, COMMENT, SHARE, REPOST, SAVE - IDHELLAM IRUKANUM
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('share/<int:post_id>/', views.share_post, name='share_post'),  # ← IDHU MUKKIYAM
    path('repost/<int:post_id>/', views.repost, name='repost'),
    path('save/<int:post_id>/', views.save_post, name='save_post'),
]