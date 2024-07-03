from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework import mixins, generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.GenericAPIView):
    """
    User Registration View
    """

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": UserSerializer(user).data},
                        status=status.HTTP_201_CREATED)
