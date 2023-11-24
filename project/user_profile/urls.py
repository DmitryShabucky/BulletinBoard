from django.urls import path
from .views import UserPostList, ProfileView, UserDetail, UserEdit

urlpatterns = [
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/profile/<int:pk>', UserDetail.as_view(), name='user_detail'),
    path('accounts/profile/<int:pk>/edit/', UserEdit.as_view(), name='user_edit'),
    path('user_posts/', UserPostList.as_view(), name='user_posts'),
]
