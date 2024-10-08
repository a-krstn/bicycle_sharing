# Generated by Django 5.0 on 2024-07-12 13:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bicycle', '0002_alter_bicycle_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(auto_now_add=True, verbose_name='Начало заказа')),
                ('stop', models.DateTimeField(auto_now=True, verbose_name='Конец заказа')),
                ('bicycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='bicycle.bicycle', verbose_name='ID транспорта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Арендатор')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
