from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

app_name = "account"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name='account/login.html', redirect_field_name="next_page",
                                                redirect_authenticated_user=True), name="login"),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address_create/', views.AddressCreatedView.as_view(), name='address_create'),
    path('delete_address/<int:pk>/', views.DeleteAddressView.as_view(), name='delete_address'),
    path('edit_address/<int:pk>/', views.EditAddressView.as_view(), name='edit_address'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html",
                                                                 success_url=reverse_lazy('account:password_reset_done'),
                                                                 # استفاده از نام مسیر
                                                                 html_email_template_name='registration/password_reset_email.html'),name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html",
                                                     success_url=reverse_lazy("account:password_reset_complete")), name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
         name='password_reset_complete'),

]
