from django.db import models
from django.utils import timezone
from unidecode import unidecode
from django.utils.text import slugify

from .utils import unique_slug_generator
from coupon.models import Discount


# Create your models here.


class Category(models.Model):
    """
    Classification of products.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            english_text = unidecode(self.name)
            self.slug = slugify(english_text)
        self.slug = unique_slug_generator(self, new_slug=self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]


class Product(models.Model):
    """
    Product model.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="category")
    name = models.CharField(max_length=100, verbose_name="اسم")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="slug")
    description = models.TextField(verbose_name="توضیحات")
    price = models.PositiveIntegerField(default=0, verbose_name="قیمت")
    inventory = models.PositiveIntegerField(default=0, verbose_name="مقدار")
    weight = models.PositiveIntegerField(default=0, verbose_name="وزن")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_final_price(self):
        """
        Calculate the final price of a product or a category
        """
        new = timezone.now()
        discounts = Discount.objects.filter(
            is_active=True,
            start_date__lte=new,
            end_date__gte=new,
        ).filter(
            models.Q(apply_to='all'),
            models.Q(apply_to='product', product=self),
            models.Q(apply_to='category', product=self.category)
        )
        final_price = self.price
        for i in discounts:
            if i.is_active:
                if i.discount_type == 'percent':
                    final_price -= (self.price * i.value / 100)
                else:
                    final_price -= i.value
        return max(int(final_price), 0)

    def save(self, *args, **kwargs):
        if not self.slug:
            english_text = unidecode(self.name)
            self.slug = slugify(english_text)
        self.slug = unique_slug_generator(self, new_slug=self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} {self.name}"

    class Meta:
        verbose_name_plural = "Products"
        ordering = ["name"]
        indexes = [
            models.Index(fields=['name', 'id']),
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]


class Feature(models.Model):
    """
    Product features
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features', verbose_name="کالا")
    name = models.CharField(max_length=255, verbose_name="ویژگی")
    value = models.CharField(max_length=255, verbose_name="مقدار")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Features"
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.name} {self.value}"


class Images(models.Model):
    """
    Product images
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="تایتل")
    image = models.ImageField(upload_to="images/", null=True, blank=True, verbose_name='عکس')
    created_at = models.DateTimeField(auto_now_add=True)
