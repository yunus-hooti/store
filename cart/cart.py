from catalog.models import Product


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
                self.cart[product_id] = {'quantity': 1, 'weight': product.weight}
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

    def total_price(self):
        total = []
        for i, j in self.cart.items():
            total.append(Product.objects.get(id=i).price * j['quantity'])
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
        cart_copy = self.cart.copy()
        for product in products:
            cart_copy[str(product.id)]['product'] = product
        for i, item in cart_copy.items():
            item['total'] = products.get(id=i).price * item['quantity']
            yield item

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True
