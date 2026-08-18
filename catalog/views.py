from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

from coupon.forms import CategoryForm
from .models import Product, Category, Feature, Images
from coupon.views import discount_products
import logging

logger = logging.getLogger('catalog')


# Create your views here.

class CategoryListView(generic.ListView):
    """
    List all categories
    """

    model = Category
    paginate_by = 20
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'


class ProductListView(generic.ListView):
    """
    List all products,
    """
    model = Product
    context_object_name = 'products'
    template_name = 'catalog/product_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        product = None
        try:
            category = Category.objects.get(slug=self.kwargs['slug'])
            product = Product.objects.filter(category=category)
        except:
            product = Product.objects.all()
        try:
            context = super().get_context_data(**kwargs)
            context['products'] = discount_products(product)
            return context
        except Exception as e:
            logger.error(f'مشکل در نمایش محصولات تخفیف خورده {e} ', exc_info=True)
            raise Exception("مشکل در نمایش محصولات تخفیف خورده")


class CreateCategoryView(UserPassesTestMixin, generic.CreateView):
    """
    Creating a category
    """
    model = Category
    template_name = 'catalog/create_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')

    def test_func(self):
        return self.request.user.is_superuser


class ProductDetailView(generic.DetailView):
    """
    detail view of a product
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            pk = self.kwargs['pk']
            product = Product.objects.get(pk=pk)
            context['product'] = discount_products([product])[0]
            return context
        except Exception as e:
            logger.error(f"مشکل در نمایش مقدار تخفیف محصول {e} ", exc_info=True)
            raise Exception("مشکل در نمایش مقدار تخفیف محصول")


class CreateProductView(UserPassesTestMixin, generic.TemplateView):
    """
    create a new product
    """
    fields = ['name', 'description', 'price', 'inventory', 'weight']
    template_name = 'catalog/create_product.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context["category"] = Category.objects.all()
            return context
        except Exception as e:
            logger.error(f"مشکل در دریافت دسته بندی ها {e} ", exc_info=True)
            raise Exception("مشکل در دریافت دسته بندی ها")

    def post(self, request, *args, **kwargs):
        """
        Save product features photos
        """
        try:
            category_product = Category.objects.get(pk=self.request.POST.get('category'))
            name_product = self.request.POST.get('name')
            description_product = self.request.POST.get('description')
            price_product = self.request.POST.get('price')
            inventory_product = self.request.POST.get('inventory')
            weight_product = self.request.POST.get('weight')
        except Exception as e:
            logger.error(f"مشکل در دریافت اطلاعات از سمت کاربر {e} ", exc_info=True)
            raise Exception("مشکل در دریافت اطلاعات از سمت کاربر")
        try:
            product_create = Product.objects.create(category=category_product, name=name_product,
                                                    description=description_product,
                                                    price=price_product, inventory=inventory_product,
                                                    weight=weight_product)
            product_create.save()
        except Exception as e:
            logger.error(f"مشکل در ساخت مخصول {e} ", exc_info=True)
            raise Exception("شکل در ساخت مخصول")

        try:
            attr_name = self.request.POST.getlist('attr_name[]')
            attr_value = self.request.POST.getlist('attr_value[]')
            for name, value in zip(attr_name, attr_value):
                if name.strip() and value.strip():
                    feature = Feature.objects.create(product=product_create, name=attr_name, value=attr_value)
                    feature.save()
        except Exception as e:
            logger.error(f"مشکل در ثبت ویژگی های مخصول {e} ", exc_info=True)
            raise Exception("مشکل در ثبت ویژگی های مخصول")
        try:
            image_product = self.request.FILES.get("image")
            image = Images.objects.create(product=product_create, image=image_product)
            image.save()
        except Exception as e:
            logger.error(f"مشکل در ذخیره عکس محصول {e} ", exc_info=True)
            raise Exception("مشکل در ذخیره عکس محصول")

        return redirect('catalog:product_list')
