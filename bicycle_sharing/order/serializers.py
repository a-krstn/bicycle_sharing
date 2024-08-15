from rest_framework import serializers
from django.utils.timezone import now

from .models import Order
from bicycle.models import Bicycle


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор заказа
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    completed = serializers.ReadOnlyField()
    bicycle = serializers.SlugRelatedField(slug_field='color',
                                           queryset=Bicycle.accessible.all())
    price = serializers.ReadOnlyField()

    def create(self, validated_data):
        validated_data['bicycle'].available = False
        validated_data['bicycle'].save()
        return Order.objects.create(**validated_data)

    class Meta:
        model = Order
        fields = ('id', 'user', 'bicycle', 'completed', 'start', 'stop', 'price')


class OrderStartSerializer(serializers.ModelSerializer):
    """
    Сериализатор начала заказа
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    bicycle = serializers.SlugRelatedField(slug_field='color',
                                           queryset=Bicycle.accessible.all())

    class Meta:
        model = Order
        fields = ('id', 'user', 'bicycle', 'start')


class OrderStopSerializer(serializers.ModelSerializer):
    """
    Сериализатор завершения заказа
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    bicycle = serializers.ReadOnlyField(source='bicycle.color')
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ('id', 'user', 'bicycle', 'completed', 'start', 'stop')

    def update(self, instance, validated_data):
        instance.completed = True
        instance.bicycle.available = True
        instance.bicycle.save()
        instance.stop = now()
        instance.save()
        return instance
