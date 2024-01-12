from django.contrib import admin

from fastfood.models import Restaurant, FastFood


@admin.register(Restaurant)
class AdminRestaurant(admin.ModelAdmin):
    list_display = ('id', 'name', 'lon', 'lat', 'address')
    list_display_links = ('id', 'name', 'lon', 'lat', 'address')
    search_fields = ('name', 'address')


@admin.register(FastFood)
class AdminFastFood(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_display_links = ('id', 'name', 'price')
    search_fields = ('name', 'price')
