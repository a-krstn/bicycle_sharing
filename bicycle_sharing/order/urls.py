from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'order'

router = routers.DefaultRouter()
router.register(r'', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    # path('', views.OrderListCreateAPIView.as_view(), name='order_start'),
    # path('stop/<int:pk>/', views.OrderStopView.as_view(), name='order_stop'),
]
