from django.contrib.auth import get_user_model
from django.db import (
    transaction,
    models
)
from apps.orders.models import (
    ProductOrderList,
    Address
)
from apps.orders.tasks import send_confirmation_email


class OrderManager(models.Manager):

    @transaction.atomic
    def create(self, *args, user, **kwargs):
        client_data = kwargs.pop('client', None)
        if client_data is not None:
            self._set_user_name(user=user, **client_data)

        product_list_data = kwargs.pop('product_list')
        address_data = kwargs.pop('address')

        total_price = self._calculate_total_price(product_list_data)

        order = super().create(
            *args,
            total_price=total_price,
            client=user,
            **kwargs
        )

        self._create_address(address_data, order)
        self._create_product_order_list(product_list_data, order)

        self._send_confirmation_email(order, user.email)

        return order

    @staticmethod
    def _set_user_name(*, user, **kwargs):
        if user.first_name is not None or user.last_name is not None:
            raise Exception('User name is already set!')

        return get_user_model().objects.update_user(instance=user, **kwargs)

    @staticmethod
    def _calculate_total_price(product_list_data):
        return sum((row['product'].price * row['quantity'] for row in product_list_data))

    @staticmethod
    def _create_address(address_data, order):
        Address.objects.create(**address_data, order=order)

    @staticmethod
    def _create_product_order_list(product_list_data, order):
        for row in product_list_data:
            ProductOrderList.objects.create(
                product=row['product'],
                quantity=row['quantity'],
                order=order
            )

    @staticmethod
    def _send_confirmation_email(order, to_email):
        send_confirmation_email.delay(order_number=order.id, to_email=to_email)

