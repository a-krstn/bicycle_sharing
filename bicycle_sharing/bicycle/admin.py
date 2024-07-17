from django.contrib import admin

from .models import Bicycle


@admin.register(Bicycle)
class BicycleAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'available')
    list_filter = ('available',)

