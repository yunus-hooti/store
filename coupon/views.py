from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic

from .models import Discount


# Create your views here.

class CouponList(UserPassesTestMixin, generic.ListView):
    """
    list all coupons
    """
    model = Discount
    context_object_name = 'discounts'
    paginate_by = 10
    template_name = 'coupon/coupon_list.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        return self.request.user.is_superuser


class CouponDetail(UserPassesTestMixin, generic.DetailView):
    """
    detail coupon
    """
    model = Discount
    context_object_name = 'discount'
    template_name = 'coupon/coupon_detail.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        return self.request.user.is_superuser

class CouponCreate(UserPassesTestMixin, generic.CreateView):
    """
    create coupon
    """
    model = Discount
    fields = '__all__'
    context_object_name = 'discount'
    template_name = 'coupon/coupon_create.html'
    success_url = reverse_lazy('catalog:product_list')
    def test_func(self):
        return self.request.user.is_superuser




