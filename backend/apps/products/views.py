import datetime

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListAPIView

from apps.products.models import Product
from apps.products.permission import IsStaffPermission
from apps.products.serializers import ProductSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'name',
                OpenApiTypes.STR,
                description='product name',
            ),
            OpenApiParameter(
                'category_name',
                OpenApiTypes.STR,
                description='product category name',
            ),
            OpenApiParameter(
                'description',
                OpenApiTypes.STR,
                description='product description',
            ),
            OpenApiParameter(
                'price_from',
                OpenApiTypes.FLOAT,
                description='price from',
            ),
            OpenApiParameter(
                'price_to',
                OpenApiTypes.FLOAT,
                description='price to',
            ),
            OpenApiParameter(
                'order_by',
                OpenApiTypes.STR,
                description='order by param',
            ),
        ]
    )
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [BasicAuthentication]

    def get_queryset(self):
        qs = super().get_queryset()
        query_params = self.get_query_params_dict()

        qs = qs.filter(
            name__icontains=query_params['name'],
            category__name__icontains=query_params['category_name'],
            description__icontains=query_params['description']
        )

        qs = qs.filter_by_price_range(
            query_params['price_from'],
            query_params['price_to']
        )

        qs = qs.order_by_ordering_param(query_params['ordering_param'])

        return qs

    def get_query_params_dict(self):
        name = self.request.query_params.get('name', '')
        category_name = self.request.query_params.get('category_name', '')
        description = self.request.query_params.get('description', '')
        price_from = self.request.query_params.get('price_from', '')
        price_to = self.request.query_params.get('price_to', '')
        ordering_param = self.request.query_params.get('order_by', None)

        return {
            'name': name,
            'category_name': category_name,
            'description': description,
            'price_from': price_from,
            'price_to': price_to,
            'ordering_param': ordering_param
        }

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffPermission()]
        else:
            return super().get_permissions()


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                'date_from',
                OpenApiTypes.STR,
                description='date from',
            ),
            OpenApiParameter(
                'date_to',
                OpenApiTypes.STR,
                description='date to',
            ),
            OpenApiParameter(
                'max_result_num',
                OpenApiTypes.INT,
                description='max results',
            ),
        ]
    )
)
class SellStatisticView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsStaffPermission]
    pagination_class = None

    @staticmethod
    def get_range_date(date_from, date_to):
        try:
            date_from = datetime.datetime.strptime(date_from, '%d-%m-%Y').date() \
                if date_from else datetime.date.today()
            date_to = datetime.datetime.strptime(date_to, '%d-%m-%Y').date() \
                if date_to else datetime.date.today()
        except ValueError:
            raise ValueError("Invalid date format. Use 'dd-mm-yyyy'.")

        return date_from, date_to

    def get_query_params_dict(self):
        date_from = self.request.query_params.get('date_from', '')
        date_to = self.request.query_params.get('date_to', '')
        max_result_num = self.request.query_params.get('max_result_num', 10)

        return {
            'date_from': date_from,
            'date_to': date_to,
            'max_result_num': max_result_num,
        }

    def get_queryset(self):
        qs = super().get_queryset()
        query_params = self.get_query_params_dict()

        date_from, date_to = self.get_range_date(
            date_from=query_params['date_from'],
            date_to=query_params['date_to']
        )
        return qs.with_total_sold(
            date_from, date_to
        ).exclude_non_sold()[:query_params['max_result_num']]

