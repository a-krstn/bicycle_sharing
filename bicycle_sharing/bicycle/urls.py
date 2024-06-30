from django.urls import path

from . import views

app_name = 'bicycle'


urlpatterns = [
    path('bicycles', views.BicycleListView.as_view(), name='bicycle_list'),

]