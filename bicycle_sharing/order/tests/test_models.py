from django.test import TestCase
from django.contrib.auth import get_user_model

from order.models import Order
from bicycle.models import Bicycle


class OrderTests(TestCase):
    """
    Тесты для модели Order
    """

    @classmethod
    def setUpTestData(cls):
        """
        Заносит данные в БД перед запуском тестов класса
        """

        user = get_user_model().objects.create_user(
            username='test_user1',
            password='12345'
        )

        bicycle = Bicycle.objects.create(
            color='Малиновый'
        )

        cls.order = Order.objects.create(
            user=user,
            bicycle=bicycle,
            completed=True,
            price=100
        )

    def test_verbose_names(self):
        """Тест параметров verbose_name"""

        # поле user
        user_real_verbose_name = self.order._meta.get_field('user').verbose_name
        user_expected_verbose_name = 'Арендатор'
        self.assertEqual(user_real_verbose_name, user_expected_verbose_name)

        # поле bicycle
        bicycle_real_verbose_name = self.order._meta.get_field('bicycle').verbose_name
        bicycle_expected_verbose_name = 'ID транспорта'
        self.assertEqual(bicycle_real_verbose_name, bicycle_expected_verbose_name)

        # поле completed
        completed_real_verbose_name = self.order._meta.get_field('completed').verbose_name
        completed_expected_verbose_name = 'Завершен'
        self.assertEqual(completed_real_verbose_name, completed_expected_verbose_name)

        # поле start
        start_real_verbose_name = self.order._meta.get_field('start').verbose_name
        start_expected_verbose_name = 'Начало заказа'
        self.assertEqual(start_real_verbose_name, start_expected_verbose_name)

        # поле stop
        stop_real_verbose_name = self.order._meta.get_field('stop').verbose_name
        stop_expected_verbose_name = 'Конец заказа'
        self.assertEqual(stop_real_verbose_name, stop_expected_verbose_name)

        # поле price
        price_real_verbose_name = self.order._meta.get_field('price').verbose_name
        price_expected_verbose_name = 'Стоимость'
        self.assertEqual(price_real_verbose_name, price_expected_verbose_name)

    def test_price_params(self):
        """Тест числовых параметров поля price"""

        real_max_digits = self.order._meta.get_field('price').max_digits
        self.assertEqual(real_max_digits, 6)

        real_decimal_places = self.order._meta.get_field('price').decimal_places
        self.assertEqual(real_decimal_places, 2)

        real_default = self.order._meta.get_field('price').default
        self.assertEqual(real_default, 0)

    def test_str_method(self):
        """Тест строкового отображения"""

        self.assertEqual(str(self.order), f'Заказ {str(self.order.pk)}')

    def test_model_verbose_name(self):
        """Тест поля verbose_name модели Order"""

        self.assertEqual(Order._meta.verbose_name, 'Заказ')

    def test_model_verbose_name_plural(self):
        """Тест поля verbose_name_plural модели Order"""

        self.assertEqual(Order._meta.verbose_name_plural, 'Заказы')
