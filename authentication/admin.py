from django.contrib import admin

from authentication.models import Activation


@admin.register(Activation)
class AdminActivation(admin.ModelAdmin):

    list_display = ('token', 'user', 'activated', 'recorded', 'updated')
    list_filter = ('user', 'activated')
    search_fields = ('user',)
    readonly_fields = ('recorded', 'updated')
    fieldsets = (
        (None, {
            'fields': ('token', 'activated'),
            'description':
            '<h4><b>*Os campos em negrito são obrigatórios.</b></h4>',
        }),
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Dados temporais', {
            'fields': ('recorded', 'updated')
        }),
    )
