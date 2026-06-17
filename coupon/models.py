from django.db import models
from django.utils import timezone

from catalog.models import Category, Product


# Create your models here.


class Discount(models.Model):
    """
    Discount by website
    """
    APPLY_TO_CHOICES = (
        ('all', 'همه مجصولات'),
        ('product', 'یک محصول'),
        ('category', 'یک دسته'),
    )
    DISCOUNT_TYPE_CHOICES = (
        ('percent', 'درصدی'),
        ('amount', 'تومانی')
    )
    title = models.CharField(max_length=100, verbose_name="عنوان کمپین")
    apply_to = models.CharField(max_length=20, choices=APPLY_TO_CHOICES, default='all', verbose_name='اعمال روی')
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, verbose_name='نوع تخفثف')
    value = models.PositiveIntegerField(default=0, verbose_name='مقدار تخفیف')
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, verbose_name='محصول')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name='دسته بندی')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        new = timezone.now()
        if self.start_date and self.start_date > new:
            return False
        if self.end_date and self.end_date > new:
            return False
        return self.is_active

    def __str__(self):
        return self.title


class DiscountCoupon(models.Model):
    """
    Discount with coupon
    """
    APPLY_TO_CHOICES = (
        ('cart', 'سبد خرید'),
        ('product', 'یک محصول'),
    )
    DISCOUNT_TYPE_CHOICES = (
        ('percent', 'درصدی'),
        ('amount', 'تومانی')
    )
    coupon = models.CharField(max_length=100, verbose_name="کوپن")
    apply_to = models.CharField(max_length=20, choices=APPLY_TO_CHOICES, default='cart', verbose_name='اعمال روی')
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, verbose_name='نوع تخفثف')
    value = models.PositiveIntegerField(default=0, verbose_name='مقدار تخفیف')
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, verbose_name='محصول')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        new = timezone.now()
        if self.start_date and self.start_date > new:
            return False
        if self.end_date and self.end_date > new:
            return False
        return self.is_active

    def __str__(self):
        return self.discount_type
