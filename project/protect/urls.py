from django.urls import path
from .views import IndexView, PostList, MainView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('user_posts/<int:pk>', PostList.as_view(), name='user_posts'),
]
