from rest_framework import serializers

from .models import Bicycle


class BicycleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Bicycle
    """

    class Meta:
        model = Bicycle
        fields = ('id', 'color')
