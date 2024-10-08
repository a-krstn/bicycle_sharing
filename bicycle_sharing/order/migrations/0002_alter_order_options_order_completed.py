# Generated by Django 5.0 on 2024-07-16 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-start',), 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AddField(
            model_name='order',
            name='completed',
            field=models.BooleanField(default=False, verbose_name='Завершен'),
        ),
    ]
