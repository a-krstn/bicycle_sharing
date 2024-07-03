from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('registration/', views.RegisterView.as_view(), name='registration'),
]
