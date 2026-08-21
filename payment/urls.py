from django.urls import  path

from . import views

app_name = "payment"

urlpatterns = [
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
    path('payment-list/',views.PaymentListView.as_view(), name='payment-list'),
]