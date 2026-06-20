from catalog.models import Product
from coupon.views import discount_products

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            if product.inventory > 0:
                old_price = product.price
                price = self.product_discount(product.id)

                self.cart[product_id] = {'quantity': 1, 'weight': product.weight, 'price': price[0].price,
                                         'old_price': str(old_price)}
        else:
            if self.cart[product_id]['quantity'] < product.inventory:
                self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease(self, product, quantity=1):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > quantity:
            self.cart[product_id]['quantity'] -= quantity
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def product_discount(self, product_id):
        return discount_products([Product.objects.get(id=product_id)])

    def total_price(self):
        total = []
        for i, j in self.cart.items():
            product_d = self.product_discount(i)
            total.append(product_d[0].price * j['quantity'])
        return sum(total)

    def price_post(self):
        total = 0
        weight = 0
        for i, j in self.cart.items():
            weight += j['weight'] * j['quantity']
        if weight == 0:
            pass
        elif weight <= 100:
            total += 20000
        elif weight <= 1000:
            total += 50000
        elif weight <= 5000:
            total += 100000
        elif weight <= 10000:
            total += 200000
        else:
            total += 500000
        return total

    def all_total_price(self):
        return self.total_price() + self.price_post()

    def get_item_count(self):
        return len(self.cart)

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_discount_list = discount_products(list(products))
        products_map = {str(p.id): p for p in products_discount_list}
        cart_copy = self.cart.copy()
        for i, item in cart_copy.items():
            product = products_map.get(i)
            if product:
                item['product'] = product
                item['total'] = product.price * item['quantity']
            else:
                item['total'] = 0
            yield item

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True
