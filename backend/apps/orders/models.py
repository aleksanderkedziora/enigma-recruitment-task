from django.db import models

from apps.orders.manager import OrderManager


class Address(models.Model):
    street = models.CharField(max_length=100)
    gate_number = models.CharField(max_length=30)
    home_number = models.CharField(max_length=30, null=True)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=30)

    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE)


class Order(models.Model):
    order_datetime = models.DateTimeField(auto_now_add=True, editable=False)
    payment_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    client = models.ForeignKey('accounts.CustomUser', on_delete=models.PROTECT, related_name='orders')
    product_list = models.ManyToManyField('products.Product', through='orders.ProductOrderList')

    objects = OrderManager()


class ProductOrderList(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
