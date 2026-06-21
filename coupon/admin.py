from django.contrib import admin

from .models import Discount,DiscountCoupon
# Register your models here.

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['title','apply_to', 'discount_type','value','is_active']

@admin.register(DiscountCoupon)
class DiscountCouponAdmin(admin.ModelAdmin):
    list_display = ['coupon','apply_to', 'discount_type','value','is_active']