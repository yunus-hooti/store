import logging

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import requests
import json

from django.urls import reverse

from cart.cart import Cart
from catalog.models import Product
from .models import Payment

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'sandbox'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


# CallbackURL = 'http://127.0.0.1:8080/verify/'


def send_request(request):
    cart = Cart(request)
    description = ''
    for i in cart:
        description += str(i['product'].name) + ", "

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": cart.total_price_next_discount(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": request.build_absolute_uri(reverse('payment:verify')),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['Authority']
            if response_json['Status'] == 100:
                reducing_inventory(request)
                Product.objects.create(user=request.user, amount=cart.total_price_next_discount(),
                                       description=description, phone=request.user.phone,status='success')
                cart.clear()
                return redirect(ZP_API_STARTPAY + authority)
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def verify(authority):
    data = {
        "MerchantID": settings.MERCHANT,
        # "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            reference_id = response_json['RefID']
            if response['Status'] == 100:
                return HttpResponse(f'successful , RefID: {reference_id}')
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def reducing_inventory(request):
    try:
        cart = Cart(request)
        for i in cart:
            product = get_object_or_404(Product, id=i['product'].id)
            product.inventory -= i['quantity']
            product.save()
    except Exception as e:
        logging.error(f"مشکل در کم کردن مقدار کالا بعد از خرید  {e}", exc_info=True)
        raise Exception("شکل در کم کردن مقدار کالا بعد از خرید ")


class PaymentListView(LoginRequiredMixin, generic.ListView):
    model = Payment
    context_object_name = 'payment'
    template_name = 'payment/payment_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_superuser:
            context['payment'] = Payment.objects.all()
        else:
            context['payment'] = Payment.objects.filter(user=self.request.user)
        return context