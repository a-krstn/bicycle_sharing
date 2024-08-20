from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from bicycle.models import Bicycle


class BicycleListTest(APITestCase):
    """
    Тесты для представления BicycleListView
    """

    @classmethod
    def setUpTestData(cls):
        """
        Заносит данные в БД перед запуском тестов класса
        """

        for i in range(1, 12):
            Bicycle.objects.create(
                color=f'color {i}'
            )

        cls.user = get_user_model().objects.create_user(username='test_user1',
                                                        password='12345')

        cls.user_token = RefreshToken.for_user(cls.user)

    def test_get_bicycle_list_without_logged_in(self):
        """
        Проверка доступа к списку велосипедов неавторизованного пользователя
        """

        response = self.client.get(reverse('bicycle:bicycle_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_bicycle_list_logged_in(self):
        """
        Проверка доступа к списку велосипедов авторизованного пользователя
        и количества записей на страницах
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user_token.access_token))
        response = self.client.get(reverse('bicycle:bicycle_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка кол-ва записей на первой странице
        self.assertEqual(len(response.data['results']), 10)

        # проверка кол-ва записей на следующей странице
        response = self.client.get(reverse('bicycle:bicycle_list') + '?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
