from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Bicycle
from .serializers import BicycleSerializer


class BicycleListView(generics.ListAPIView):
    """
    Bicycle List View
    """

    queryset = Bicycle.accessible.filter(available=True)
    serializer_class = BicycleSerializer
    permission_classes = (IsAuthenticated,)
