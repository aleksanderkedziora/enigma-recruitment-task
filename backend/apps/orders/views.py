from apps.orders.models import Order
from apps.orders.permission import IsCustomerPermission
from apps.orders.serializers import OrderListSerializer, OrderCreateSerializer

from rest_framework.authentication import BasicAuthentication

from rest_framework import (
    viewsets,
    mixins,
)

from rest_framework.permissions import IsAuthenticated


class OrderViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [IsCustomerPermission()]
        else:
            return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return super().get_serializer_class()
