from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import User,AddressUser

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['phone','first_name', 'is_active','is_staff']
    ordering = ['phone']
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('email','first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password1','password2')}),
        ('Personal info', {'fields': ('email','first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )

@admin.register(AddressUser)
class AddressUserAdmin(admin.ModelAdmin):
    list_display = ['user','phone_number','first_name','province']
