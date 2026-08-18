from django.urls import path


from . import views
from .views import CreateCategoryView

app_name = 'catalog'

urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('create_category', CreateCategoryView.as_view(), name='create_category'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<str:slug>', views.ProductListView.as_view(), name='product_list_category'),
    path('Product_detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('create_product/', views.CreateProductView.as_view(), name='create_product'),
]
