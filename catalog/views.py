
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy, reverse

from .models import Product, Category, Feature, Images
from coupon.views import discount_products

# Create your views here.

class ProductListView(generic.ListView):
    """
    List all products,
    """
    model = Product
    context_object_name = 'products'
    template_name = 'catalog/product_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = discount_products(Product.objects.all())
        return context

class ProductDetailView(generic.DetailView):
    """
    detail view of a product
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = "product"


class CreateProductView(generic.TemplateView):
    """
    create a new product
    """
    fields = ['name', 'description', 'price', 'inventory', 'weight']
    template_name = 'catalog/create_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        """
        Save product features photos
        """
        category_product = Category.objects.get(pk=self.request.POST.get('category'))
        name_product = self.request.POST.get('name')
        description_product = self.request.POST.get('description')
        price_product = self.request.POST.get('price')
        inventory_product = self.request.POST.get('inventory')
        weight_product = self.request.POST.get('weight')
        try:
            product_create = Product.objects.create(category=category_product, name=name_product,
                                                    description=description_product,
                                                    price=price_product, inventory=inventory_product,
                                                    weight=weight_product)
            product_create.save()
        except Exception as e:
            raise ValueError(e)
        attr_name = self.request.POST.getlist('attr_name[]')
        attr_value = self.request.POST.getlist('attr_value[]')
        for name, value in zip(attr_name, attr_value):
            if name.strip() and value.strip():
                feature = Feature.objects.create(product=product_create, name=attr_name, value=attr_value)
                feature.save()
        image_product = self.request.FILES.get("image")
        image = Images.objects.create(product=product_create, image=image_product)
        image.save()

        return redirect('catalog:product_list')
