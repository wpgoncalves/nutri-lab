from hashlib import sha256
from os.path import join

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from authentication.models import Activation
from authentication.utils import email_html, form_is_valid


def registration(request):

    if request.user.is_authenticated:
        return redirect('/')

    method = request.method

    if method == 'GET':
        return render(request, 'authentication/registration.html')
    elif method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        token = sha256(f'{username}{email}'.encode()).hexdigest()

        if not form_is_valid(request, username, email, password, confirm_password):  # noqa: E501
            return redirect('authentication:registration')

        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            is_active=False)
            user.save()

            activation = Activation(token=token, user=user)
            activation.save()

            path_template = join(settings.BASE_DIR,
                                 'authentication/templates/authentication/email-active-user.html')  # noqa: E501

            email_html(path_template, 'Cadastro confirmado', [email, ],
                       username=username, activation_link=f'127.0.0.1:8000/auth/user_activation/{token}')  # noqa: E501

            messages.add_message(request, messages.SUCCESS,
                                 "Cadastro realizado com sucesso!")

            return redirect('authentication:login')

        except IntegrityError:
            messages.add_message(request, messages.WARNING,
                                 'Nome de usuário já existente! Não é possível mais de um usuário com mesmo nome!')  # noqa: E501
            return redirect('authentication:registration')
        except Exception as e:  # noqa: E722
            messages.add_message(request, messages.ERROR, e)  # noqa: E501
            return redirect('authentication:registration')


def login(request):

    if request.user.is_authenticated:
        return redirect('/')

    method = request.method

    if method == "GET":
        return render(request, 'authentication/login.html')
    elif method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if not user:
            messages.add_message(request, messages.WARNING,
                                 'Username ou senha inválidos!')
            return redirect('authentication:login')
        else:
            auth.login(request, user)
            return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('authentication:login')


def user_activation(request, token):

    token = get_object_or_404(Activation, token=token)

    if token.activated:
        messages.add_message(request, messages.WARNING,
                             'Este token já foi usado!')
        return redirect('authentication:login')

    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()

    token.activated = True
    token.save()

    messages.add_message(request, messages.SUCCESS,
                         'Conta ativada com sucesso!')
    return redirect('authentication:login')
