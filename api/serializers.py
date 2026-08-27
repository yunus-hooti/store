from rest_framework import serializers
from catalog.models import Product


class ProductSerializerList(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'inventory', 'weight']

class ProductSerializerDetail(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['category', 'name','description', 'price', 'inventory', 'weight']