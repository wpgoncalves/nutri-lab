from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from re import search

from django.contrib import messages


def form_is_valid(request, username, email, password, confirm_password):

    if not username.strip():
        messages.add_message(request, messages.ERROR,
                             'Por favor, informe seu nome de usuário!')
        return False

    if not email.strip():
        messages.add_message(request, messages.ERROR,
                             'Por favor, informe um endereço de e-mail válido!')  # noqa: E501
        return False

    if len(password) < 6:
        messages.add_message(request, messages.ERROR,
                             'Sua senha deve conter 6 ou mais caractertes.')
        return False

    if not password == confirm_password:
        messages.add_message(request, messages.ERROR,
                             'As senhas não coincidem. Tente novamente!')
        return False

    if not search('[A-Z]', password):
        messages.add_message(request, messages.ERROR,
                             'Sua senha não contem letras maiúsculas.')
        return False

    if not search('[a-z]', password):
        messages.add_message(request, messages.ERROR,
                             'Sua senha não contem letras minúsculas.')
        return False

    if not search('[1-9]', password):
        messages.add_message(request, messages.ERROR,
                             'Sua senha não contém números')
        return False

    return True


def email_html(path_template: str, subject: str, to: list, **kwargs) -> dict:

    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, to)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}
