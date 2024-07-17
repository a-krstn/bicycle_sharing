from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .serializers import OrderSerializer, OrderStopSerializer
from .models import Order


class OrderStartView(generics.GenericAPIView):
    """
    Начало аренды велосипеда
    """

    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Вывод всех заказов (по идее тут должен выводиться список доступных велосипедов)
        """

        orders = Order.objects.filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response({"orders": serializer.data},
                        status=status.HTTP_200_OK)

    def post(self, request):
        current_user_last_order = request.user.orders.first()
        if current_user_last_order and not current_user_last_order.completed:
            return Response({"error": "Для аренды другого велосипеда завершите текущую поездку"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"order": serializer.data},
                        status=status.HTTP_201_CREATED)


class OrderStopView(generics.GenericAPIView):
    """
    Завершение аренды велосипеда
    """

    serializer_class = OrderStopSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method PUT is not allowed"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = Order.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Instance does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

        if instance.completed:
            return Response({"error": "Заказ уже завершен"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"order": serializer.data},
                        status=status.HTTP_201_CREATED)

