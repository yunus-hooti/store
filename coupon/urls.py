from django.urls import  path

from . import views


app_name = 'coupon'
urlpatterns = [
    path('', views.CouponList.as_view(), name='coupon_list'),
    path('coupon-detail/<int:pk>/',views.CouponDetail.as_view(), name='coupon_detail'),
    path('coupon-create/',views.CouponCreate.as_view(), name='coupon_create'),
]