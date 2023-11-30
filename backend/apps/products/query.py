import datetime

from django.db import models
from django.db.models import Subquery, OuterRef, Sum
from django.http import Http404


class ProductQuerySet(models.QuerySet):
    def annotate_with_total_sold(self, date_from: datetime.date, date_to: datetime.date) -> models.QuerySet:
        """Annotates product with total sold quantity in requested period of time."""
        product_list_subquery = self.get_product_list_subquery(date_from, date_to)
        return self.annotate(total_sold=Subquery(product_list_subquery))

    @staticmethod
    def get_product_list_subquery(date_from: datetime.date, date_to: datetime.date) -> models.QuerySet:
        from apps.orders.models import ProductOrderList

        queryset = ProductOrderList.objects.filter(
            product=OuterRef('pk'),
        ).values('product').annotate(
            total_quantity=Sum('quantity')
        ).values('total_quantity')

        if date_from is not None:
            queryset = queryset.filter(order__order_date__gte=date_from)

        if date_to is not None:
            queryset = queryset.filter(order__order_date__lte=date_to)

        return queryset

    def exclude_non_sold(self) -> models.QuerySet:
        """Excludes products which are not sold in requested period of time"""
        return self.exclude(total_sold=0)

    def filter_by_price_range(self, price_from: str, price_to: str) -> models.QuerySet:
        """Handles and filters queryset by price range"""
        queryset = self

        try:
            if price_from:
                price_from = float(price_from)
                queryset = queryset.filter(pricea__gte=price_from)

            if price_to:
                price_to = float(price_to)
                queryset = queryset.filter(pricea__lte=price_to)

            return queryset

        except ValueError as e:
            raise Http404(e)

    def order_by_ordering_param(self,
                                ordering_param: str,
                                extra_ordering_params: dict[str, str] = None,
                                order_dir: str = 'ASC') -> models.QuerySet:
        """Handles and filters queryset by price range"""
        ordering_param_dict_map = {
            'name': 'name',
            'category': 'category__id',
            'price': 'price'
        }

        if extra_ordering_params is not None:
            ordering_param_dict_map.update(extra_ordering_params)

        order_direction_dict_map = {
            'ASC': '',
            'DESC': '-'
        }

        ordering_param_val = ordering_param_dict_map.get(ordering_param, None)
        ordering_direction_val = order_direction_dict_map.get(order_dir.upper(), '')

        return self.order_by(f'{ordering_direction_val}{ordering_param_val}') \
            if ordering_param_val is not None else self
