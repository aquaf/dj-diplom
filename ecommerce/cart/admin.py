from django.contrib import admin
from .models import Cart, Order


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    fields = ('user', 'products', 'total', 'purchased',)
    list_display = ('user', 'total', 'purchased',)


class OrderInline(admin.TabularInline):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ('timestamp',)
    list_display = ('order_num', 'user', 'timestamp', 'total',)
    filter_horizontal = ('products',)