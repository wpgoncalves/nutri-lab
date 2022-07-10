from django.contrib.auth.models import User
from django.db import models


class Activation(models.Model):

    token = models.CharField(verbose_name="Token", max_length=64,
                             primary_key=True, unique=True)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                             verbose_name='Usuário')

    activated = models.BooleanField(verbose_name="Ativado",
                                    default=False)

    recorded = models.DateTimeField(verbose_name='Gravado em',
                                    auto_now_add=True)

    updated = models.DateTimeField(verbose_name='Atualizado em',
                                   auto_now=True)

    class Meta:
        ordering = ['user']
        verbose_name = 'Ativação'
        verbose_name_plural = 'Ativações'

    def __str__(self):
        return self.user.username
