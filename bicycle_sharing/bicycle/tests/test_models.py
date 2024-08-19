from django.test import TestCase

from bicycle.models import Bicycle


class BicycleTests(TestCase):
    """
    Тесты для модели Bicycle
    """

    @classmethod
    def setUpTestData(cls):
        """
        Заносит данные в БД перед запуском тестов класса
        """

        cls.bicycle = Bicycle.objects.create(
            color='Малиновый'
        )
        cls.color_field = cls.bicycle._meta.get_field('color')

    def test_verbose_name(self):
        """Тест параметра verbose_name"""

        real_verbose_name = getattr(self.color_field, 'verbose_name')
        expected_verbose_name = 'Цвет'
        self.assertEqual(real_verbose_name, expected_verbose_name)

    def test_max_length(self):
        """Тест параметра max_length"""

        real_max_length = getattr(self.color_field, 'max_length')
        self.assertEqual(real_max_length, 30)

    def test_str_method(self):
        """Тест строкового отображения"""

        self.assertEqual(str(self.bicycle), str(self.bicycle.color))

    def test_model_verbose_name(self):
        """Тест поля verbose_name модели Bicycle"""

        self.assertEqual(Bicycle._meta.verbose_name, 'Велосипед')

    def test_model_verbose_name_plural(self):
        """Тест поля verbose_name_plural модели Bicycle"""

        self.assertEqual(Bicycle._meta.verbose_name_plural, 'Велосипеды')
