from django.db import models
from django.db.models import Subquery, OuterRef, Sum


class ProductQuerySet(models.QuerySet):
    def with_total_sold(self, date_from, date_to):
        product_list_subquery = self.get_product_list_subquery(date_from, date_to)
        return self.annotate(total_sold=Subquery(product_list_subquery))

    @staticmethod
    def get_product_list_subquery(date_from, date_to):
        from apps.orders.models import ProductOrderList

        return ProductOrderList.objects.filter(
            product=OuterRef('pk'),
            order__order_date__range=(date_from, date_to)
        ).values('product').annotate(
            total_quantity=Sum('quantity')
        ).values('total_quantity')

    def exclude_non_sold(self):
        return self.exclude(total_sold=0)

    def filter_by_price_range(self, price_from, price_to):
        qs = self

        try:
            if price_from:
                price_from = float(price_from)
                qs = self.filter(pricea__gte=price_from)

            if price_to:
                price_to = float(price_to)
                qs = qs.filter(pricea__lte=price_to)

                return qs

        except ValueError:
            raise ValueError("Invalid value for price. Must be a valid float.")

    def order_by_ordering_param(self, ordering_param):
        dict_map = {
            'name': 'name',
            'category': 'category__name',
            'price': 'price'
        }

        ordering_param_val = dict_map.get(ordering_param, None)
        return self.order_by(ordering_param_val) if ordering_param_val is not None else self
