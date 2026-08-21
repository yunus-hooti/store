from django.db import models

from account.models import User

# Create your models here.


class Payment(models.Model):
    """
    User transactions
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='payments',verbose_name='کاربر')
    amount = models.PositiveIntegerField(default=0,verbose_name='قیمت کل')
    description = models.CharField(max_length=250,verbose_name='توضحیات')
    phone = models.CharField(max_length=11,verbose_name='شماره')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}-{self.description}"

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش ها"
