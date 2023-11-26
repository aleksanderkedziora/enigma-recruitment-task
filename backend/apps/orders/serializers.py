from rest_framework import serializers

from apps.orders.models import Order, Address, ProductOrderList


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


class ProductOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrderList
        fields = [
            'id',
            'product',
            'quantity',
        ]
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    customer_first_name = serializers.CharField(max_length=100)
    customer_last_name = serializers.CharField(max_length=100)
    address = AddressSerializer()
    product_list = ProductOrderListSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'total_price',
            'client',
            'payment_date',
            'customer_first_name',
            'customer_last_name',
            'address',
            'product_list'
        ]

        read_only_fields = [
            'id',
            'total_price',
            'client',
            'payment_date'
        ]
