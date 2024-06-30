from django.db import models


class AvailableModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)


class Bicycle(models.Model):
    """
    Модель велосипеда
    """

    color = models.CharField(max_length=30, verbose_name='Цвет')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    objects = models.Manager()
    accessible = AvailableModel()

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'Велосипеды'
        verbose_name_plural = 'Велосипеды'
