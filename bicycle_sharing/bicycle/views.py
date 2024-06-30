from django.shortcuts import render
from rest_framework import generics

from .models import Bicycle
from .serializers import BicycleSerializer


class BicycleListView(generics.ListAPIView):
    queryset = Bicycle.accessible.all()
    serializer_class = BicycleSerializer

