from rest_framework import serializers

from apps.products.models import Product


class BaseProductSerializer(serializers.ModelSerializer):
    """Serializes product object."""
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category']
        read_only_fields = ['id']


class ListProductSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        model = Product
        fields = BaseProductSerializer.Meta.fields + ['thumbnail']


class ProductSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        model = Product
        fields = BaseProductSerializer.Meta.fields + ['image', 'description']


class ProductInOrderWriteSerializer(serializers.Serializer):
    """Nested serializer to use in Order serializer."""
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    quantity = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ['product', 'quantity']


class StatisticProductSerializer(ProductSerializer):
    total_sold = serializers.SerializerMethodField()

    class Meta(BaseProductSerializer):
        model = Product
        fields = BaseProductSerializer.Meta.fields + ['total_sold']

    @staticmethod
    def get_total_sold(obj) -> int:
        return obj.total_sold
