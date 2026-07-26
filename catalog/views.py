from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic

from .models import Product, Category, Feature, Images
from coupon.views import discount_products
import logging

logger = logging.getLogger('catalog')


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
        try:
            context = super().get_context_data(**kwargs)
            context['products'] = discount_products(Product.objects.all())
            return context
        except:
            logger.error('مشکل در نمایش محصولات تخفیف خورده', exc_info=True)
            raise Http404


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
        except:
            logger.error("مشکل در نمایش مقدار تخفیف محصول ", exc_info=True)
            raise Http404


class CreateProductView(generic.TemplateView):
    """
    create a new product
    """
    fields = ['name', 'description', 'price', 'inventory', 'weight']
    template_name = 'catalog/create_product.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context["category"] = Category.objects.all()
            return context
        except:
            logger.error("مشکل در دریافت دسته بندی ها ", exc_info=True)
            raise Http404

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
            logger.error("مشکل در دریافت اطلاعات از سمت کاربر", exc_info=True)
            raise Http404
        try:
            product_create = Product.objects.create(category=category_product, name=name_product,
                                                    description=description_product,
                                                    price=price_product, inventory=inventory_product,
                                                    weight=weight_product)
            product_create.save()
        except Exception as e:
            logger.error("مشکل در ساخت مخصول", exc_info=True)
            raise ValueError(e)

        try:
            attr_name = self.request.POST.getlist('attr_name[]')
            attr_value = self.request.POST.getlist('attr_value[]')
            for name, value in zip(attr_name, attr_value):
                if name.strip() and value.strip():
                    feature = Feature.objects.create(product=product_create, name=attr_name, value=attr_value)
                    feature.save()
        except Exception as e:
            logger.error("مشکل در ثبت ویژگی های مخصول", exc_info=True)
            raise Http404
        try:
            image_product = self.request.FILES.get("image")
            image = Images.objects.create(product=product_create, image=image_product)
            image.save()
        except Exception as e:
            logger.error("مشکل در ذخیره عکس محصول")
            raise Http404

        return redirect('catalog:product_list')
