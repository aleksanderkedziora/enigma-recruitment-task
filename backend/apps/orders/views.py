from apps.orders.models import Order
from apps.orders.permission import IsCustomerPermission
from apps.orders.serializers import OrderSerializer

from rest_framework.authentication import BasicAuthentication

from rest_framework import (
    viewsets,
    mixins,
)

from rest_framework.permissions import IsAuthenticated


class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [IsCustomerPermission()]
        else:
            return super().get_permissions()

