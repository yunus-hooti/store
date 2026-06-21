from django.urls import  path

from . import views


app_name = 'coupon'
urlpatterns = [
    path('', views.CouponList.as_view(), name='coupon_list'),
    path('coupon-detail/<int:pk>/',views.CouponDetail.as_view(), name='coupon_detail'),
    path('discount-coupon-detail/<int:pk>/',views.DiscountCouponDetail.as_view(), name='discount_coupon_detail'),
    path('coupon-create/',views.CouponCreate.as_view(), name='coupon_create'),
    path('coupon-delete/<int:pk>/',views.DeleteCoupon.as_view(), name='coupon_delete'),
    path('discount-coupon-delete/<int:pk>/',views.DeleteDiscountCoupon.as_view(), name='discount_coupon_delete'),
    path('coupon-edit/<int:pk>/',views.EditCoupon.as_view(), name='coupon_edit'),
    path('discount-coupon-edit/<int:pk>/',views.EditDiscountCoupon.as_view(), name='discount_coupon_edit'),
    path('coupon-create-user/',views.UserDiscountCouponView.as_view(), name='coupon_create_user'),

]