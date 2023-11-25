from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from board.models import Post
from board.views import AuthenticationContextMixin, PostList
from user_profile.forms import UserForm

class ProfileView(AuthenticationContextMixin, TemplateView):
    template_name = 'user_profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user).order_by('-created')
        return context

class UserDetail(AuthenticationContextMixin, DetailView):
    model = User
    template_name = 'user_profile/user_detail.html'
    context_object_name = 'user_detail'

class UserEdit(AuthenticationContextMixin, UpdateView):

    model = User
    form_class = UserForm
    template_name = 'user_profile/profile_edit.html'

    def get_success_url(self):
        return reverse ('user_edit', args=[str(self.request.user.id)])

class UserPostList(PostList):

    template_name = 'user_profile/user_posts.html'

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user).order_by('-created')
        return queryset


class PostDetail(AuthenticationContextMixin, DetailView):
    model = Post
    template_name = 'posts/post.html'
    context_object_name = 'user_post'