from django.shortcuts import get_object_or_404
from rest_framework import  viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication  import BasicAuthentication

from order.models import Order
from catalog.models import Product
from payment.models import Payment
from .serializers import ProductSerializerList, ProductSerializerDetail, PaymentSerializerList, PaymentSerializerDetail, \
    OrderSerializerList, OrderSerializerDetail


# Create your views here.


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('category').all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializerList
        return ProductSerializerDetail


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PaymentSerializerDetail
        return PaymentSerializerList

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def report(self, request):
        payment_id = request.query_params.get('id')
        if payment_id:
            payment = get_object_or_404(Payment, pk=payment_id)
            serializer = PaymentSerializerDetail(payment)
            return Response(serializer.data)

        queryset = Payment.objects.all()
        user_id = request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(created__range=[start_date, end_date])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderSerializerDetail
        return OrderSerializerList

    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.prefetch_related('items__product')
        if user.is_superuser:
            return qs
        return qs.filter(user=user)
