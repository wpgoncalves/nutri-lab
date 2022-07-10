from django.urls import path

from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_activation/<str:token>', views.user_activation,
         name='user-activation')
]
