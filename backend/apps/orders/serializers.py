from rest_framework import serializers

from apps.accounts.serializers import UserSerializer, OrderUserSerializer
from apps.orders.models import Order, Address, ProductOrderList
from apps.products.serializers import ProductInOrderWriteSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'street',
            'gate_number',
            'home_number',
            'zip_code',
            'city'
        ]
        read_only_fields = ['id']


class ProductOrderListReadSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.ReadOnlyField(source='product.id')

    class Meta:
        model = ProductOrderList
        fields = [
            'product',
            'quantity',
        ]


class OrderListSerializer(serializers.ModelSerializer):
    client = OrderUserSerializer()
    address = AddressSerializer()

    product_list = ProductOrderListReadSerializer(
            source='productorderlist_set',
            many=True,
            read_only=True
        )

    class Meta:
        model = Order
        fields = [
            'id',
            'total_price',
            'client',
            'payment_date',
            'address',
            'product_list'
        ]

        read_only_fields = [
            'id',
            'total_price',
            'client',
            'payment_date'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    client = OrderUserSerializer(required=False)
    address = AddressSerializer()

    product_list = ProductInOrderWriteSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'total_price',
            'client',
            'payment_date',
            'address',
            'product_list'
        ]

        read_only_fields = [
            'id',
            'total_price',
            'client',
            'payment_date'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        order = Order.objects.create(
            user=user,
            **validated_data
        )
        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        product_order_list_serializer = ProductOrderListReadSerializer(
            data=instance.productorderlist_set.all(), many=True
        )
        product_order_list_serializer.is_valid()

        representation['product_list'] = product_order_list_serializer.data
        return representation
