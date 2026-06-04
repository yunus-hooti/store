from django.urls import path


from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('Product_detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('create_product/', views.CreateProductView.as_view(), name='create_product'),
]
