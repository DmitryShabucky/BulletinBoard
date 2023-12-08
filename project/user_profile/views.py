from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from django.contrib import messages

from board.models import Post, Reply, Category
from board.views import NewReplyContextMixin, PostList, ReplyList
from user_profile.forms import UserForm
from project import settings


class ProfileView(NewReplyContextMixin, TemplateView):
    template_name = 'user_profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['posts'] = Post.objects.filter(author=self.request.user).order_by('-created')
        context['new_replies'] = Reply.objects.filter(post__author=self.request.user, status=False).order_by('-created')
        context['replies'] = Reply.objects.filter(post__author=self.request.user).order_by('-created')
        context['user_replies'] = Reply.objects.filter(user=self.request.user)
        context['categories'] = user.categories.all()
        return context


class UserDetail(NewReplyContextMixin, DetailView):
    model = User
    template_name = 'user_profile/user_detail.html'
    context_object_name = 'user_detail'


class UserEdit(NewReplyContextMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_profile/profile_edit.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Данные изменены!')
        return response

    def get_success_url(self):
        return reverse('user_edit', args=[str(self.request.user.id)])


class UserPostList(PostList):
    template_name = 'user_profile/user_posts.html'

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user).order_by('-created')
        return queryset


class UserReplyList(NewReplyContextMixin, ListView):
    model = Reply
    template_name = 'user_profile/user_reply_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_posts'] = Post.objects.filter(author=self.request.user).order_by('-created').distinct()
        context['new_replies'] = Reply.objects.filter(post__author=self.request.user, status=False).order_by('-created')
        context['replies'] = Reply.objects.filter(post__author=self.request.user).order_by('-created')
        return context


class UserNewReplyList(UserReplyList):
    template_name = 'user_profile/user_reply_new.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        context['post'] = post
        if self.kwargs['type'] == 'new':
            context['replies'] = Reply.objects.filter(post=post, status=False).order_by('-created')
        elif self.kwargs['type'] == 'all':
            context['replies'] = Reply.objects.filter(post=post).order_by('-created')
        return context

class UserLeftRelpyList(UserReplyList):

    template_name = 'user_profile/user_left_reply_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(replies__user=self.request.user).distinct()
        context['replies'] = Reply.objects.filter(user=self.request.user).order_by('-created')
        return context


def reply_update_status(request, id, type):
    reply = get_object_or_404(Reply, id=id)
    post = reply.post
    post_url = f'{settings.SITE_URL}/post/{post.id}'
    if type == 'public':
        reply.status_update()
        messages.success(request,'Отклик опубликован')
        html_content = render_to_string(
            'reply/reply_confirm_email.html',
            {
                'post': post,
                'user': reply.user,
                'url': post_url,
                'reply': reply,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{post.title}',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[reply.user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        reply.delete()
        messages.success(request, 'Отклик удален')
        if request.user.id != reply.user.id:
            html_content = render_to_string(
                'reply/reply_delete_email.html',
                {
                    'post': post,
                    'user': reply.user,
                    'url': post_url,
                    'reply':reply,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{post.title}',
                body=f'',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[reply.user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class UserCategoryList(ListView):

    model = Category
    template_name = 'user_profile/user_category_list.html'
    context_object_name = 'categories'


    def get_queryset(self):
        user = self.request.user
        queryset = user.categories.all()
        return queryset

