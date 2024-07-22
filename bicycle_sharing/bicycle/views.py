from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import pagination

from .models import Bicycle
from .serializers import BicycleSerializer


class BicyclePagination(pagination.PageNumberPagination):
    """
    Класс пагинации для модели Bicycle
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BicycleListView(generics.ListAPIView):
    """
    Bicycle List View
    """

    queryset = Bicycle.accessible.filter(available=True)
    serializer_class = BicycleSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = BicyclePagination
