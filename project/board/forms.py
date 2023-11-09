from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.messages.views import SuccessMessageMixin

from .models import Post, Category, Reply


class PostForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Выберите категорию'
    )
    title = forms.CharField(
        label='Заголовок:'
    )
    content = forms.CharField(
        widget=CKEditorUploadingWidget,
        label='Контент'
    )
    class Meta:
        model = Post
        fields = ['category', 'title', 'content']


class ReplyForm(forms.ModelForm, SuccessMessageMixin):
    class Meta:
        model = Reply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'text': '',
        }
        success_message = "Отклик оставлен. Ожидайте модерации."

