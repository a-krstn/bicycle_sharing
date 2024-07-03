from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Registration Serializer
    """

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(validated_data['username'],
                                                    validated_data['email'],
                                                    validated_data['password'])
        return user
