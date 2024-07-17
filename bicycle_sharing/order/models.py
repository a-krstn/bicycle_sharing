from django.db import models
from django.contrib.auth import get_user_model

from bicycle.models import Bicycle


class Order(models.Model):
    """
    Модель заказа велосипеда
    """

    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='orders',
                             verbose_name='Арендатор')
    bicycle = models.ForeignKey(Bicycle,
                                on_delete=models.CASCADE,
                                related_name='orders',
                                verbose_name='ID транспорта')
    completed = models.BooleanField(default=False,
                                    verbose_name='Завершен')
    start = models.DateTimeField(auto_now_add=True,
                                 verbose_name='Начало заказа')
    stop = models.DateTimeField(auto_now=True,
                                verbose_name='Конец заказа')

    def __str__(self):
        return f'Заказ {self.pk}'

    def total_cost(self):
        """
        Возвращает стоимость аренды по таксе
        """
        pass

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ("-start",)
