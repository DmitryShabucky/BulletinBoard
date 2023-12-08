from django.urls import path
from .views import PostList, PostDetail, PostCreate, ReplyList, CategoryList, LoginWarning, PostEdit, PostDelete, update_subscription


urlpatterns = [
    path('warning/', LoginWarning.as_view(), name='login_warning'),
    path('', PostList.as_view(), name='posts'),
    path('post/<int:pk>', PostDetail.as_view(), name='post'),
    path('post/<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('post/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/reply', ReplyList.as_view(), name='reply_list'),
    path('post/category/<int:pk>', CategoryList.as_view(), name='category'),
    path('post/category/<int:id>/<str:type>', update_subscription, name='category_subscription'),

]