from rest_framework import serializers
from django.utils.timezone import now

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор заказа
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    completed = serializers.ReadOnlyField()

    def create(self, validated_data):
        validated_data['bicycle'].available = False
        validated_data['bicycle'].save()
        return Order.objects.create(**validated_data)

    class Meta:
        model = Order
        fields = ('id', 'user', 'bicycle', 'completed', 'start', 'stop')


class OrderStopSerializer(serializers.ModelSerializer):
    """
    Сериализатор завершения заказа
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ('id', 'user', 'completed', 'start', 'stop')

    def update(self, instance, validated_data):
        instance.completed = True
        instance.bicycle.available = True
        instance.bicycle.save()
        instance.stop = now()
        instance.save()
        return instance
