from django.contrib import admin
from .models import Order, OrderProduct, Payment

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment', 'order_number', 'order_total', 'status', 'is_ordered', 'created_at']
    list_editable = ('status',)
    list_filter = ('user', 'status', 'is_ordered', 'created_at')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)
