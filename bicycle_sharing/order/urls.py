from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('', views.OrderStartView.as_view(), name='order_start'),
    path('stop/<int:pk>/', views.OrderStopView.as_view(), name='order_stop'),
]
