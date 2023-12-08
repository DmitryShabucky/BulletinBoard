from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from board.models import Post
from django.template.loader import render_to_string

from project import settings
from board.utils import send_report


@receiver(post_save, sender=Post)
def report_a_new_post(sender, instance, **kwargs):
    category = instance.category
    subscribers = category.subscribers.all()
    subscribers_emails = []
    subscribers_emails += [s.email for s in subscribers]

    send_report(instance.pk, instance.title, subscribers_emails)
