# from django.contrib.auth.mixins import LoginRequiredMixin
import os

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)
from django.views.generic.edit import FormMixin

from .models import Post, Reply, Category
from .forms import PostForm, ReplyForm


# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'protect/index.html'

# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['is_not_author']= not self.request.protect.groups.filter(name= 'author').exists()
#     return context

class AuthenticationContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = User.objects.filter(id=self.request.user.id).exists()
        return context


class PostList(AuthenticationContextMixin, ListView):
    model = Post
    ordering = '-created'
    template_name = 'posts/posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ReplyList(AuthenticationContextMixin, ListView):
    model = Reply
    template_name = 'reply/reply_list.html'
    context_object_name = 'replies'
    paginate_by = 10

    def get_queryset(self):
        self.post = get_object_or_404(Post, id=self.kwargs['pk'])
        queryset = Reply.objects.filter(Q(post=self.post, status=True) |
                                        Q(post=self.post, user=self.request.user, status=False) |
                                        Q(post=self.post, post__author=self.request.user, status=False)).order_by(
            '-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.post = get_object_or_404(Post, id=self.kwargs['pk'])
        context['post'] = self.post
        return context


class PostDetail(AuthenticationContextMixin, FormMixin, DetailView):
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
            post_url = request.build_absolute_uri(reverse('main'))
            # send_mail(
            #     subject=f'{post.title}',
            #     message=f'Пользователь {request.user} Оставил отклик: {reply.text[:15:].title()}...\n Читать отклик {post_url}',
            #     from_email='dmz.sh@yandex.ru',
            #     recipient_list=[post.author.email],
            # )
            html_content = render_to_string(
                'reply/reply_email.html',
                {
                    'post': post,
                    'user': reply.user,
                    'url': post_url,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'{post.title}',
                body=f'Пользователь {request.user} Оставил отклик: {reply.text[:15:].title()}...\n Читать отклик {post_url}',
                from_email=os.getenv('DEFAULT_FROM_EMAIL'),
                to=[post.author.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect('post', post.id)

        else:
            return ReplyForm


class PostCreate(AuthenticationContextMixin,CreateView, PermissionRequiredMixin):
    permission_required = ('board.add_post',)
    permission_denied_message = 'Для создания объявления необходимо пройти регистрацию на портале.'
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryList(AuthenticationContextMixin, ListView):
    model = Category
    template_name = 'category/category.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=self.category)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'board.delete_post'
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('')


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.edit_post')
    ...


class ReplyEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.edit_rebly')
    ...


class ReplyDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_reply')
    ...
class LoginWarning(TemplateView):

    template_name = 'login_warning.html'