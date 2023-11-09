# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)
from django.views.generic.edit import FormMixin

from .models import Post, Reply
from .forms import PostForm, ReplyForm


# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'protect/index.html'

# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['is_not_author']= not self.request.user.groups.filter(name= 'author').exists()
#     return context


class PostList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'posts/posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = User.objects.filter(id=self.request.user.id).exists()
        return context


class ReplyList(ListView):
    model = Reply
    template_name = 'reply/reply_list.html'
    context_object_name = 'replies'
    paginate_by = 10

    def get_queryset(self):
        self.post = get_object_or_404(Post, id=self.kwargs['pk'])
        queryset = Reply.objects.filter(post=self.post).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.post = get_object_or_404(Post, id=self.kwargs['pk'])
        context['post'] = self.post
        return context


class PostDetail(FormMixin, DetailView):
    form_class = ReplyForm
    model = Post
    template_name = 'posts/post.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['pk'])
        form = self.get_form()
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.user = request.user
            reply.save()
            return redirect('post', post.id)
        else:
            return ReplyForm


class PostCreate(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
