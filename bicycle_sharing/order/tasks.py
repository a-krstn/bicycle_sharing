from celery import shared_task
from django.shortcuts import get_object_or_404
from dateutil.relativedelta import relativedelta

from decimal import *

from .models import Order


getcontext().prec = 2


@shared_task
def get_total_cost(order_id):
    """
    Расчет стоимости поездки
    """

    order = get_object_or_404(Order, pk=order_id)
    rental_time = relativedelta(order.stop, order.start)
    total_cost = (rental_time.hours * 60 + rental_time.minutes + round(rental_time.seconds / 60)) * Decimal(7.6)
    order.price = Decimal(str(total_cost)).quantize(Decimal("1.00"))
    order.save()
