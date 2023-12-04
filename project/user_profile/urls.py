from django.urls import path
from .views import (UserPostList, ProfileView, UserDetail, UserEdit, UserReplyList, reply_update_status,
                    UserNewReplyList, UserLeftRelpyList
                    )

urlpatterns = [
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/profile/<int:pk>', UserDetail.as_view(), name='user_detail'),
    path('accounts/profile/<int:pk>/edit/', UserEdit.as_view(), name='user_edit'),
    path('accounts/profile/replies', UserReplyList.as_view(), name='user_replies'),
    path('accounts/profile/replies/left', UserLeftRelpyList.as_view(), name='user_replies_left'),
    path('accounts/profile/replies/post/<int:pk>/<str:type>', UserNewReplyList.as_view(), name='user_reply_new'),
    path('accounts/profile/reply/<int:id>/<str:type>', reply_update_status, name='user_reply_update'),
    path('accounts/profile/user_posts/', UserPostList.as_view(), name='user_posts'),

]
