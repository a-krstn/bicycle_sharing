from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, permissions, pagination, viewsets, mixins
from rest_framework.response import Response

from .serializers import OrderSerializer, OrderStartSerializer, OrderStopSerializer
from .models import Order
from .tasks import get_total_cost


class OrderPagination(pagination.PageNumberPagination):
    """
    Класс пагинации для модели Order
    """

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


# class OrderListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     pagination_class = OrderPagination
#
#     def get_queryset(self):
#         if self.request.method == 'GET':
#             print('Таки да')
#         return Order.objects.filter(user=self.request.user)
#
#     def create(self, request, *args, **kwargs):
#         current_user_last_order = request.user.orders.first()
#         if current_user_last_order and not current_user_last_order.completed:
#             return Response({"error": "Для аренды другого велосипеда завершите текущую поездку"},
#                             status=status.HTTP_400_BAD_REQUEST)
#         return super().create(request, *args, **kwargs)


# class OrderStartView(generics.GenericAPIView):
#     """
#     Начало аренды велосипеда
#     """
#
#     serializer_class = OrderSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     pagination_class = OrderPagination
#
#     def get(self, request):
#         """
#         Вывод всех заказов (по идее тут должен выводиться список доступных велосипедов)
#         """
#
#         orders = Order.objects.filter(user=request.user)
#         page = self.get_p
#         serializer = self.get_serializer(orders, many=True)
#         return Response({"orders": serializer.data},
#                         status=status.HTTP_200_OK)
#
#     def post(self, request):
#         current_user_last_order = request.user.orders.first()
#         if current_user_last_order and not current_user_last_order.completed:
#             return Response({"error": "Для аренды другого велосипеда завершите текущую поездку"},
#                             status=status.HTTP_400_BAD_REQUEST)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"order": serializer.data},
#                         status=status.HTTP_201_CREATED)


# class OrderStopView(generics.GenericAPIView):
#     """
#     Завершение аренды велосипеда
#     """
#
#     serializer_class = OrderStopSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({"error": "Method PUT is not allowed"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         try:
#             instance = Order.objects.get(pk=pk)
#         except ObjectDoesNotExist:
#             return Response({"error": "Instance does not exist"},
#                             status=status.HTTP_404_NOT_FOUND)
#
#         if instance.completed:
#             return Response({"error": "Заказ уже завершен"},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = self.get_serializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         get_total_cost.delay(instance.pk)
#         return Response({"order": serializer.data},
#                         status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin):
    """
    Order ViewSet
    """

    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = OrderPagination

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderStartSerializer
        if self.action == 'update':
            return OrderStopSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        current_user_last_order = request.user.orders.first()
        if current_user_last_order and not current_user_last_order.completed:
            return Response({"error": "Для аренды другого велосипеда завершите текущую поездку"},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.completed:
            return Response({"error": "Заказ уже завершен"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        get_total_cost.delay(instance.pk)
        return Response({"order": serializer.data},
                        status=status.HTTP_200_OK)
