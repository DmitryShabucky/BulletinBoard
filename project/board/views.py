import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
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
from project import settings


class NewReplyContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['new_replies'] = Reply.objects.filter(post__author=self.request.user, status=False)
        return context


class PostList(NewReplyContextMixin, ListView):
    model = Post
    ordering = '-created'
    template_name = 'posts/posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetail(NewReplyContextMixin, DetailView):

    model = Post
    template_name = 'posts/post.html'
    context_object_name = 'post'

class PostCreate(NewReplyContextMixin,CreateView, PermissionRequiredMixin):
    permission_required = ('board.add_post',)
    permission_denied_message = 'Для создания объявления необходимо пройти регистрацию на портале.'
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Объявление создано')
        return super().form_valid(form)

class PostEdit(UpdateView):

    form_class = PostForm
    model = Post
    template_name = 'posts/post_edit.html'


    def form_valid(self, form):
        messages.success(self.request, 'Объявление изменено')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_posts')

class PostDelete(DeleteView):

    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('user_posts')

    def form_valid(self, form):
        messages.success(self.request, 'Объявление Удалено')
        return super().form_valid(form)


class ReplyList(NewReplyContextMixin, ListView, FormMixin):
    form_class = ReplyForm
    model = Reply
    template_name = 'reply/reply_list.html'
    context_object_name = 'replies'

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['pk'])
        form = self.get_form()
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.user = request.user
            if post.author.id == reply.user.id:
                reply.status=True
            reply.save()
            messages.success(request, 'Отклик оставлен!')
            post_url =f'{settings.SITE_URL}/post/{post.id}'

            if self.request.user.id != post.author.id:
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
                    body=f'Пользователь {request.user} Оставил отклик: {reply.text[:15:].title()}... Читать отклик {post_url}',
                    from_email=os.getenv('DEFAULT_FROM_EMAIL'),
                    to=[post.author.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect('reply_list', post.id)
            return redirect('reply_list', post.id)
        else:
            self.form_invalid(form)

    def get_queryset(self):
        self.post = get_object_or_404(Post, id=self.kwargs['pk'])
        queryset = Reply.objects.filter(Q(post=self.post, status=True)|Q(post=self.post, user=self.request.user, status=False)|Q(post=self.post, post__author=self.request.user, status=False)).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.post = get_object_or_404(Post, id=self.kwargs['pk'])
        context['post'] = self.post
        return context




class CategoryList(NewReplyContextMixin, ListView):
    model = Category
    template_name = 'category/category.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['posts'] = Post.objects.filter(category=self.category)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        return context

@login_required
def update_subscription(request, id, type):
    category = get_object_or_404(Category, id=id)
    if type == 'subscribe':
        category.subscribers.add(request.user)
        messages.success(request, f'Вы подписались на рассылку новостей категории "{category}"')
        return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        category.subscribers.remove(request.user)
        messages.success(request, f'Вы отписались от рассылки новостей категории "{category}"')
        return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class LoginWarning(TemplateView):

    template_name = 'login_warning.html'