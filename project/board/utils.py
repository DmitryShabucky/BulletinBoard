from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from project import settings


def send_report(pk, title, subscribers):

    html_content = render_to_string(
        'posts/post_create_email.html',
        {
            'text':title,
            'link':f"{settings.SITE_URL}/post/{pk}"
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
