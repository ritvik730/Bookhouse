from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def mail_sent(context):
    html_content = render_to_string('email_verify.html', context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        context['header'],
        text_content,
        settings.EMAIL_HOST_USER,
        [context['email']]

    )
    email.attach_alternative(html_content, 'text/html')
    email.send()


def mail_to_admin(context):
    html_content = render_to_string('contact_mail.html', context)
    text_content = strip_tags(html_content)
    mail = 'bookhouse229@gmail.com'
    email = EmailMultiAlternatives(
        "Contact Form",
        text_content,
        settings.EMAIL_HOST_USER,
        [mail]

    )
    email.attach_alternative(html_content, 'text/html')
    email.send()
