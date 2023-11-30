from django.contrib import admin

from apps.orders.models import Address, Order, ProductOrderList

admin.site.register(Address)
admin.site.register(Order)
admin.site.register(ProductOrderList)

