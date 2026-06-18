from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone

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

    def form_valid(self, form):
        apply_to = form.cleaned_data['apply_to']
        if Discount.objects.filter(apply_to=apply_to).exists():
            messages.success(self.request, 'این نوع تخفیف برای کالا یا کل وجود دارد ')
            return self.form_invalid(form)
        messages.success(self.request, 'تخفیف با موفقیت ثبت شد ')
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


def discount_products(list_product):
    """
    it takes a list of products and applies a discount to the products that have a discount and returns a list of them
    :param list_product:
    :return: list_product
    """
    current_time = timezone.now()
    discounts = Discount.objects.filter(
        is_active=True,
        start_date__lte=current_time,
        end_date__gte=current_time,
    )
    global_discount = discounts.filter(apply_to='all')
    if global_discount:
        discounts = global_discount
    else:
        discounts = discounts.exclude(apply_to='all')

    list_product_discount = []
    for discount in discounts:
        if discount.apply_to == 'all':
            for i in list_product:
                if discount.discount_type == 'percent':
                    discount_amount = (i.price * discount.value) // 100
                    i.price = i.price - discount_amount
                elif discount.discount_type == 'amount':
                    discount_amount = i.price - discount.value
                    if discount_amount > 0:
                        i.price = discount_amount
                list_product_discount.append(i)
            break

        elif discount.apply_to == 'product':
            for i in list_product:
                if discount.product == i:
                    if discount.discount_type == 'percent':
                        discount_amount = i.price - ((i.price * discount.value) // 100)
                        i.price = discount_amount
                elif discount.discount_type == 'amount':
                    discount_amount = i.price - discount.value
                    if discount_amount > 0:
                        i.price = discount_amount

                list_product_discount.append(i)

        elif discount.apply_to == 'category':
            for i in list_product:
                if i.category == discount.category:
                    if discount.discount_type == 'percent':
                        discount_amount = (i.price * discount.value) / 100
                        i.price = discount_amount
                    elif discount.discount_type == 'amount':
                        discount_amount = i.price - discount.value
                        if discount_amount > 0:
                            i.price = discount_amount

                list_product_discount.append(i)
    return list_product


class DeleteCoupon(UserPassesTestMixin, generic.DeleteView):
    """
    delete coupon
    """
    model = Discount
    template_name = 'coupon/ok_delete_coupon.html'
    success_url = reverse_lazy('coupon:coupon_list')

    def test_func(self):
        return self.request.user.is_superuser


class EditCoupon(UserPassesTestMixin, generic.UpdateView):
    """
    edit coupon
    """
    model = Discount
    template_name = 'coupon/coupon_create.html'
    fields = '__all__'
    success_url = reverse_lazy('coupon:coupon_list')

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context