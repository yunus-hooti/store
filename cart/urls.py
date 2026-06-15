from django.urls import path

from cart import views
app_name = 'cart'
urlpatterns = [
    path('add-cart/<int:id>/',views.AddCart.as_view(), name='add_cart'),
    path('detail/',views.CartDetailView.as_view(), name='detail_cart'),
    path('cart-update/', views.CartUpdateView.as_view(), name='cart_update'),

]