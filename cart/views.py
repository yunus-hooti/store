from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from catalog.models import Product


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
        context['total_price'] = cart.total_price()
        return context




class CartUpdateView(View):
    """
    Update a cart.
    """
    def post(self, request, *args, **kwargs):  # استفاده از *args, **kwargs برای انعطاف‌پذیری بیشتر
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        if not product_id or not action:
            return JsonResponse({'success': False, 'error': 'Missing product_id or action'}, status=400)

        try:
            product = get_object_or_404(Product, pk=product_id)
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
            updated_item_total_price = cart.cart.get(str(product_id), {}).get('total_price', 0)
            # updated_post_price_car = cart.post_price_car  # فرض می‌کنیم این متد در کلاس Cart وجود دارد

            return JsonResponse({
                'success': True,
                'quantity': updated_quantity,
                'item_total_price': updated_item_total_price,
                # 'post_price_car': updated_post_price_car,
                'total_price': cart.total_price(),  # فرض می‌کنیم این متد در کلاس Cart وجود دارد
                'cart_count': len(cart.cart),
                'action': action  # برای دیباگ مفید است
            })

        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
        except Exception as e:
            # لاگ کردن خطا برای دیباگ
            print(f"Error updating cart: {e}")
            return JsonResponse({'success': False, 'error': 'An internal error occurred'}, status=500)
