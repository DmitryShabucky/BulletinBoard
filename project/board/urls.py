from django.urls import path
from .views import PostList, PostDetail, PostCreate, ReplyList


urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/reply', ReplyList.as_view(), name='reply_list'),
]