from rest_framework import serializers

from catalog.models import Product
from payment.models import Payment
from order.models import Order, OrderItem


class ProductSerializerList(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'inventory', 'weight']


class ProductSerializerDetail(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'inventory', 'weight']


class PaymentSerializerList(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['user', 'phone', 'amount', 'status']


class PaymentSerializerDetail(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['user', 'description', 'phone', 'amount', 'status']


class OrderSerializerList(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment', 'status']


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_purchase']


class OrderSerializerDetail(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    address_user = serializers.StringRelatedField()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'address_user', 'total_amount', 'discount_amount', 'final_amount', 'post_price',
                  'transaction_id', 'payment', 'status', 'items']
