from rest_framework import generics, viewsets

from catalog.models import Product
from .serializers import ProductSerializerList,ProductSerializerDetail

# Create your views here.


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('category').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializerList
        return ProductSerializerDetail