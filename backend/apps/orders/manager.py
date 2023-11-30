from __future__ import annotations
from typing import TYPE_CHECKING, OrderedDict

from django.contrib.auth import get_user_model
from django.db import (
    transaction,
    models
)

from apps.orders.tasks import send_confirmation_email
from apps.products.models import Product

from decimal import Decimal

if TYPE_CHECKING:
    UserModel = get_user_model()
    from models import (
        Order,
    )


class OrderManager(models.Manager):

    @transaction.atomic
    def create(self, *args, user: UserModel, **kwargs) -> Order:
        """Creates order with related objects and finally sends mail via Celery"""
        customer_data = kwargs.pop('customer', None)
        if customer_data is not None:
            self._set_user_name(user=user, **customer_data)

        product_list_data = kwargs.pop('product_list')
        address_data = kwargs.pop('address')

        total_price = self._calculate_total_price(product_list_data)

        order = super().create(
            *args,
            total_price=total_price,
            customer=user,
            **kwargs
        )

        self._create_address(address_data, order)
        self._create_product_order_list(product_list_data, order)

        self._send_confirmation_email(order, user.email)

        return order

    @staticmethod
    def _set_user_name(*, user: UserModel, **kwargs) -> None:
        """Sets user first and last name data if it is blank"""
        if user.first_name is not None or user.last_name is not None:
            raise Exception('User name is already set!')

        return get_user_model().objects.update_user(instance=user, **kwargs)

    @staticmethod
    def _calculate_total_price(product_list_data: list[OrderedDict[Product, int]]) -> Decimal:
        """Sums prices of all products in order 'cart'."""
        return sum((row['product'].price * row['quantity'] for row in product_list_data)) # noqa it's Decimal not int

    @staticmethod
    def _create_address(address_data: dict, order: Order) -> None:
        """Saves customer address as object."""
        from apps.orders.models import Address

        Address.objects.create(**address_data, order=order)

    @staticmethod
    def _create_product_order_list(product_list_data: list, order: Order) -> None:
        """Saves product and quantity as a 'row' od 'order product list'."""
        from apps.orders.models import ProductOrderList

        for row in product_list_data:
            ProductOrderList.objects.create(
                product=row['product'],
                quantity=row['quantity'],
                order=order
            )

    @staticmethod
    def _send_confirmation_email(order: Order, to_email: str) -> None:
        """Sends async email with order confirmation and order details."""
        send_confirmation_email.delay(order_number=order.id, to_email=to_email)

