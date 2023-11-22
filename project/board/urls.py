from django.urls import path
from .views import PostList, PostDetail, PostCreate, ReplyList, CategoryList, LoginWarning


urlpatterns = [
    path('warning/', LoginWarning.as_view(), name='login_warning'),
    path('posts/', PostList.as_view(), name='posts'),
    path('post/<int:pk>', PostDetail.as_view(), name='post'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/reply', ReplyList.as_view(), name='reply_list'),
    path('post/category/<int:pk>', CategoryList.as_view(), name='category'),

]