from django.contrib import admin

from .models import Product, Category, Feature, Images


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'inventory','price']


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['product','name','value']

@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image']