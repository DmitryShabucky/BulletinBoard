from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from positions import POSITIONS


class Category(models.Model):
    name = models.CharField(max_length=20, choices=POSITIONS, unique=True, verbose_name='Категории')

    def __str__(self):
        return self.get_name_display()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='user')
    title = models.CharField('Заголовок', max_length=250, null=False)
    content = RichTextUploadingField(null=True)
    created = models.DateTimeField("Дата публикации", auto_now_add=True)
    updated = models.DateTimeField("Дата обновления", auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория', related_name='categories')

    def __str__(self):
        return f'{self.title}. {self.content}. Опубликовано: {self.created.date()}'

    def get_absolute_url(self):
        return reverse('post', args=[int(self.pk)])


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.text}. Добавлено: {self.created.date()}. Автор: {self.user.username} '

    def get_absolute_url(self):
        return reverse('post', args=[int(self.pk)])

    def status_update(self):
        self.status = True
        self.save()

