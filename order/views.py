from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

import logging

from account.models import AddressUser
from catalog.models import Product
from .models import Order, OrderItem
from cart.cart import Cart


# Create your views here.


class OrderCreateView(LoginRequiredMixin, View):
    """
    Creating the order model after user confirmation and clearing the shopping cart.
    """

    def get(self, request):
        try:
            cart = Cart(request)
            address_user = AddressUser.objects.filter(user=request.user)
            return render(request, 'order/checkout.html',
                          {'cart': cart, 'address_user': address_user, 'quantity': len(cart.cart)})
        except AddressUser.DoesNotExist:
            logging.error("مشکل در ارسال  اطلاعت",exc_info=True)
            raise Exception("مشکل در ارسال  اطلاعت")

    def post(self, request):
        cart = Cart(request)
        address_id = request.POST.get('address_id')
        address = get_object_or_404(AddressUser, id=address_id)
        try:
            order = Order.objects.create(
                user=request.user,
                address_user=address,
                total_amount=cart.total_price(),
                discount_amount=cart.total_price_next_discount(),
                final_amount=cart.all_total_price(),
                post_price=cart.price_post()

            )
            order.save()
        except Exception as e:
            logging.error(f"مشکل در ذخیره سفارش {e} ",exc_info=True)
            raise Exception("مشکل در ذخیره سفارش")
        try:
            for p_id, item in cart.cart.items():
                product = get_object_or_404(Product, id=p_id)
                item_order = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price_at_purchase=item['price'],
                )

                item_order.save()

            cart.clear()
            return redirect('catalog:product_list')
        except Exception as e:
            logging.error(f"مشکل در ثبت آیتم سفارش ها {e} ",exc_info=True)
            raise Exception("مشکل در ثبت آیتم سفارش ها")

class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    context_object_name = "orders"
    template_name = 'order/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created')


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        context['discount'] = order.total_amount - order.discount_amount
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
