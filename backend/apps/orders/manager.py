from django.db import models
from django.db import transaction


class OrderManager(models.Manager):

    @transaction.atomic
    def create(self, *args, **kwargs):
        from apps.orders.models import ProductOrderList

        product_data = kwargs.pop('product_data', None)

        order = super().create(*args, **kwargs)

        for product_id, quantity in product_data:
            ProductOrderList.objects.create(
                product_id=product_id,
                quantity=quantity,
                order=order
            )

        return order
