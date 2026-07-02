from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('order_create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order_list/', views.OrderListView.as_view(), name='order_list'),
    path('order_detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]