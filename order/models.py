from django.db import models

from account.models import User, AddressUser
from catalog.models import Product

import string
import random


# Create your models here.

class Order(models.Model):
    """
    Order data recording model following order finalization
    """
    Product_status = (
        ('در حال پردازش', 'در حال پردازش'),
        ('آماده برای ارسال', 'آماده برای ارسال'),
        ('محصول ارسال شد', 'محصول ارسال شد'),
        ('تحویل پست داده شد', 'تحویل پست داده شد'),
        ('محصول به مشتری تحویل داده شد', 'محصول به مشتری تحویل داده شد'),
        ('لغو توسط مشتری', 'لغو توسط مشتری'),
        ('لغو توسط فروشنده', 'لغو توسط فروشنده'),
        ('مرحوع شد', 'مرحوع شد')
    )
    user = models.ForeignKey(User, related_name='users', on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    address_user = models.ForeignKey(AddressUser, related_name='address_user', on_delete=models.SET_NULL, null=True,
                                     verbose_name='آدرس')

    total_amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت کل')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='بعد تخفیف')
    final_amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت نهای')
    post_price = models.DecimalField(max_digits=10, default=0, decimal_places=0, null=True, blank=True,
                                     verbose_name='هزینه پستی')

    transaction_id = models.CharField(max_length=100,unique=True, blank=True, null=True, verbose_name='کد پیگیری')
    payment = models.BooleanField(default=False, verbose_name='پرداخت')
    status = models.CharField(choices=Product_status, default='در حال پردازش', verbose_name='وضعیت سفارش')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.transaction_id = self._generate_code()
        super().save(*args, **kwargs)

    def _generate_code(self):
        code = ''
        for i in range(1,9):
            code += str(random.randint(0,9))
        return code

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name_plural = 'سفارش ها'


class OrderItem(models.Model):
    """
    Order item storage model
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='مخصولات')
    quantity = models.PositiveIntegerField(default=1, verbose_name='مقدار محصول')
    price_at_purchase = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت زمان خرید')

    class Meta:
        verbose_name_plural = 'آیتم سفارش ها'

    def __str__(self):
        return f"{self.quantity} X {self.product.name}"
