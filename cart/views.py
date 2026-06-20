from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from catalog.models import Product
from coupon.views import discount_products

# Create your views here.

class AddCart(View):
    """
    Add a cart to the cart.
    """
    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        print(product)
        cart = Cart(request)
        cart.add(product)
        return redirect("cart:detail_cart")


class CartDetailView(TemplateView):
    """
    Detail view of a cart.
    """
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        context['all_total_price'] = cart.all_total_price()
        context['total_price'] = cart.total_price()
        context['price_post'] = cart.price_post()
        return context




class CartUpdateView(View):
    """
    Update a cart.
    """
    def post(self, request, *args, **kwargs):  # استفاده از *args, **kwargs برای انعطاف‌پذیری بیشتر
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        product = get_object_or_404(Product, pk=product_id)

        if not product_id or not action:
            return JsonResponse({'success': False, 'error': 'Missing product_id or action'}, status=400)

        try:
            cart = Cart(request)  # اطمینان حاصل کنید که Cart درست مقداردهی می‌شود (مثلاً با session)

            if action == 'add':
                cart.add(product)
            elif action == 'remove':
                cart.remove(product)
            elif action == 'decrease':
                cart.decrease(product)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)

            # اطمینان حاصل کنید که این متدها وجود دارند و مقادیر صحیح برمی‌گردانند
            updated_quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
            product_ids = cart.cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            discount_products_list = discount_products(products)
            product_map = {str(p.id): p for p in discount_products_list}
            current_product = product_map.get(str(product_id))
            if current_product:
                total_ = current_product.price * updated_quantity
            else:
                total_ = 0
            return JsonResponse({
                'success': True,
                'quantity': updated_quantity,
                'price_post': cart.price_post(),
                'total_':total_,
                'total_price': cart.total_price(),  # فرض می‌کنیم این متد در کلاس Cart وجود دارد
                'cart_count': len(cart.cart),
                'all_total_price':cart.all_total_price(),
                'action': action  # برای دیباگ مفید است
            })

        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
        except Exception as e:
            # لاگ کردن خطا برای دیباگ
            print(f"Error updating cart: {e}")
            return JsonResponse({'success': False, 'error': 'An internal error occurred'}, status=500)
