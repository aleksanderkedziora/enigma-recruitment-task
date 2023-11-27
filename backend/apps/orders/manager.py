from django.contrib.auth import get_user_model
from django.db import models
from django.db import transaction
from django.db.models import Sum
from rest_framework.exceptions import ValidationError

from apps.products.models import Product


class OrderManager(models.Manager):

    @transaction.atomic
    def create(self, *args, user, **kwargs):
        from apps.orders.models import ProductOrderList, Address

        client_data = kwargs.pop('client', None)
        if client_data is not None:
            self._set_user_name(user=user, **client_data)

        product_list_data = kwargs.pop('product_list')
        address_data = kwargs.pop('address')

        total_price = sum((row['id'].price_netto * row['quantity'] for row in product_list_data))

        order = super().create(
            *args,
            total_price=total_price,
            client=user,
            **kwargs
        )
        Address.objects.create(**address_data, order=order)

        for row in product_list_data:
            ProductOrderList.objects.create(
                product=row['id'],
                quantity=row['quantity'],
                order=order
            )

        return order

    @staticmethod
    def _set_user_name(*, user, **kwargs):
        if user.first_name is not None or user.last_name is not None:
            raise Exception('User name is already set!')

        return get_user_model().objects.update_user(instance=user, **kwargs)
