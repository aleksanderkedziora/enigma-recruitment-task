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

from apps.products.models import Product, ProductCategory
from apps.products.permission import IsStaffPermission
from apps.products.serializers import (
    ProductSerializer,
    ListProductSerializer,
    StatisticProductSerializer
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'name',
                OpenApiTypes.STR,
                description='product name',
            ),
            OpenApiParameter(
                'description',
                OpenApiTypes.STR,
                description='product description',
            ),
            OpenApiParameter(
                'category',
                OpenApiTypes.INT, enum=list(ProductCategory.objects.values_list('id', flat=True)),
                description='Filter by category id.',
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
            OpenApiParameter(
                'order_dir',
                OpenApiTypes.STR, enum=['ASC', 'DESC'],
                description='if 1 sort descending, if 0 sort ascending',
            ),
        ]
    )
)
class ProductViewSet(viewsets.ModelViewSet):
    """Base viewset for manage and see product attributes."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [BasicAuthentication]

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.get_query_params_dict()

        queryset = queryset.filter(
            name__icontains=query_params['name'],
            description__icontains=query_params['description']
        )

        if query_params['category'] is not None:
            queryset = queryset.filter(category_id=query_params['category'])

        queryset = queryset.filter_by_price_range(
            query_params['price_from'],
            query_params['price_to']
        )

        queryset = queryset.order_by_ordering_param(
            query_params['ordering_param'],
            order_dir=query_params['order_dir']
        )

        return queryset

    def get_query_params_dict(self):
        name = self.request.query_params.get('name', '')
        category = self.request.query_params.get('category', None)
        description = self.request.query_params.get('description', '')
        price_from = self.request.query_params.get('price_from', '')
        price_to = self.request.query_params.get('price_to', '')
        ordering_param = self.request.query_params.get('order_by', None)
        order_dir = self.request.query_params.get('order_dir', 'ASC')

        return {
            'name': name,
            'category': category,
            'description': description,
            'price_from': price_from,
            'price_to': price_to,
            'ordering_param': ordering_param,
            'order_dir': order_dir
        }

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffPermission()]
        else:
            return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return ListProductSerializer

        return super().get_serializer_class()


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
            OpenApiParameter(
                'order_dir',
                OpenApiTypes.STR, enum=['ASC', 'DESC'],
                description='if 1 sort descending, if 0 sort ascending',
            ),
        ]
    )
)
class SellStatisticView(ListAPIView):
    """View for get list for bes sold products in required time period."""

    queryset = Product.objects.all()
    serializer_class = StatisticProductSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsStaffPermission]
    pagination_class = None

    @staticmethod
    def get_range_date(date_from: str, date_to: str) -> tuple[datetime.date, datetime.date]:
        try:
            date_from = datetime.datetime.strptime(date_from, '%d-%m-%Y').date() \
                if date_from else None
            date_to = datetime.datetime.strptime(date_to, '%d-%m-%Y').date() \
                if date_to else None
        except ValueError:
            raise ValueError("Invalid date format. Use 'dd-mm-yyyy'.")

        return date_from, date_to

    def get_query_params_dict(self):
        date_from = self.request.query_params.get('date_from', '')
        date_to = self.request.query_params.get('date_to', '')
        max_result_num = self.request.query_params.get('max_result_num', 10)
        order_dir = self.request.query_params.get('order_dir', 'DESC')

        return {
            'date_from': date_from,
            'date_to': date_to,
            'max_result_num': max_result_num,
            'order_dir': order_dir
        }

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.get_query_params_dict()

        date_from, date_to = self.get_range_date(
            date_from=query_params['date_from'],
            date_to=query_params['date_to']
        )

        try:
            max_results = int(query_params['max_result_num'])
        except ValueError:
            max_results = None

        queryset = queryset.annotate_with_total_sold(
            date_from, date_to
        ).exclude_non_sold()

        queryset = queryset.order_by_ordering_param(
            'total_sold',
            extra_ordering_params={'total_sold': 'total_sold'},
            order_dir=query_params['order_dir']
        )

        if max_results is not None:
            return queryset[:max_results]

        return queryset
