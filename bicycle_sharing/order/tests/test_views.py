from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from order.models import Order
from order.serializers import OrderSerializer
from order.views import OrderPagination
from bicycle.models import Bicycle


class OrderViewSetTest(APITestCase):
    """
    Тесты для представления OrderViewSet
    """

    @classmethod
    def setUpTestData(cls):
        """
        Заносит данные в БД перед запуском тестов класса
        """

        cls.user_1 = get_user_model().objects.create_user(username='test_user1',
                                                          password='12345')
        cls.user_2 = get_user_model().objects.create_user(username='test_user2',
                                                          password='12345')

        cls.user_1_token = RefreshToken.for_user(cls.user_1)
        cls.user_2_token = RefreshToken.for_user(cls.user_2)

        cls.bicycle = Bicycle.objects.create(color='Малиновый')

        # создание нескольких завершенных заказов пользователя user1
        for i in range(1, 8):
            Order.objects.create(
                bicycle=cls.bicycle,
                user=cls.user_1,
                completed=True,
                price=10 * i
            )

        # создание одного незавершенного заказа пользователя user2
        cls.not_completed_order = Order.objects.create(
                bicycle=cls.bicycle,
                user=cls.user_2,
                completed=False,
                price=0
            )

    def test_get_order_list_without_logged_in(self):
        """
        Проверка доступа к списку заказов неавторизованного пользователя
        """

        response = self.client.get(reverse('order:order-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_list_logged_in(self):
        """
        Проверка доступа к списку заказов авторизованного пользователя
        и количества записей на страницах
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user_1_token.access_token))
        response = self.client.get(reverse('order:order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка кол-ва записей на первой странице
        self.assertEqual(len(response.data['results']), 5)

        # проверка кол-ва записей на следующей странице
        response = self.client.get(reverse('order:order-list') + '?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_new_order_without_logged_in(self):
        """
        Проверка доступа к созданию нового заказа неавторизованным пользователем
        """

        data = {
            'bicycle': self.bicycle,
            'user': self.user_1,
            'completed': True,
            'price': 20
        }

        response = self.client.post(reverse('order:order-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_new_order_logged_in(self):
        """
        Проверка доступа к созданию нового заказа авторизованным пользователем
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user_1_token.access_token))

        data = {
            'bicycle': self.bicycle,
            'user': self.user_1,
            'completed': True,
            'price': 20
        }

        response = self.client.post(reverse('order:order-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # проверка создания нового заказа при наличии незавершенного текущего заказа
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user_2_token.access_token))

        data = {
            'bicycle': self.bicycle,
            'user': self.user_2,
            'completed': True,
            'price': 20
        }

        response = self.client.post(reverse('order:order-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_without_logged_in(self):
        """
        Проверка доступа к изменению существующего заказа неавторизованного пользователя
        """

        response = self.client.put(reverse('order:order-detail', args=(self.not_completed_order.pk,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_order_logged_in(self):
        """
        Проверка доступа к завершению текущего заказа авторизованным пользователем
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user_1_token.access_token))

        # попытка завершения текущего заказа пользователя user_2 пользователем user_1
        response = self.client.put(reverse('order:order-detail', args=(self.not_completed_order.pk,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # завершение текущего заказа пользователем user_2
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.user_2_token.access_token))

        response = self.client.put(reverse('order:order-detail', args=(self.not_completed_order.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # попытка вновь завершить уже завершенный заказ
        response = self.client.put(reverse('order:order-detail', args=(self.not_completed_order.pk,)))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
