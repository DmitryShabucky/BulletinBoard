from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from board.models import Post

class MainView(TemplateView):
    template_name = 'main.html'

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    # def get_queryset(self):
    #     self.protect = get_object_or_404(User, id=self.kwargs['pk'])
    #     queryset = Post.objects.filter(author=self.protect).order_by('-created')
    #     return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user).order_by('-created')
        context['is_authenticated'] = User.objects.filter(id=self.request.user.id).exists()
        return context

class PostList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'protect/user_posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = User.objects.filter(id=self.request.user.id).exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'posts/post.html'
    context_object_name = 'user_post'