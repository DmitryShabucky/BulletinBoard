from allauth.account.adapter import DefaultAccountAdapter
from random import randint

from django.core.mail import send_mail
from project.settings import DEFAULT_FROM_EMAIL


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        code = int(randint(1000, 9999))
        subject = "Верификация электронной почты"
        message = f"Код подтверждения: {code}"
        # Send the email using your preferred method, e.g., Django's send_mail or a third-party service
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [email])