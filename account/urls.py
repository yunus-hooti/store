from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = "account"

urlpatterns = [
    path("login/", LoginView.as_view(template_name='account/login.html', redirect_field_name="next_page",
                                     redirect_authenticated_user=True), name="login"),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address_create/', views.AddressCreatedView.as_view(), name='address_create'),
    path('delete_address/<int:pk>/', views.DeleteAddressView.as_view(), name='delete_address'),
    path('edit_address/<int:pk>/', views.EditAddressView.as_view(), name='edit_address'),

]
