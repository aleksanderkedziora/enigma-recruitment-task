from rest_framework import viewsets

from apps.products.models import Product
from apps.products.permission import IsStaffPermission
from apps.products.serializers import ProductSerializer

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication


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

    qs_name_filters = [
        'name'
        'category__name',
        'description',
    ]

    def get_queryset(self):
        name = self.request.query_params.get('name', '')
        category_name = self.request.query_params.get('category_name', '')
        description = self.request.query_params.get('description', '')

        price_from = self.request.query_params.get('price_from', '')
        price_to = self.request.query_params.get('price_to', '')

        qs = super().get_queryset()

        if price_from != '':
            qs = qs.filter(price_netto__gte=float(price_from))

        if price_to != '':
            qs = qs.filter(price_netto__lte=float(price_to))

        ordering_param = self.request.query_params.get('order_by', None)

        if ordering_param:
            if ordering_param == 'name':
                qs = qs.order_by(ordering_param)
            elif ordering_param == 'category':
                qs = qs.order_by('category__name')
            elif ordering_param == 'price':
                qs = qs.order_by('price_netto')

        return qs.filter(
            name__icontains=name,
            category__name__icontains=category_name,
            description__icontains=description
        )

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffPermission()]
        else:
            return super().get_permissions()
