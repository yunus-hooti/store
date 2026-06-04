from django import forms
from .models import User, AddressUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['phone', 'first_name', 'last_name']


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['phone', 'first_name', 'last_name']


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError("رمز عبور یکی نیستن")
        return password_confirm


# class AddressCreatedForm(forms.ModelForm):
#     class Meta:
#         model = AddressUser
#         fields = ['phone_number', 'first_name', 'last_name', 'province', 'city', 'cod_post']

class AddressCreatedForm(forms.ModelForm):
    class Meta:
        model = AddressUser
        # مطمئن شو که این فیلدها دقیقاً با نام فیلدهای مدل Address مطابقت دارند
        fields = ["first_name", "last_name", "phone_number", "province", "city", "cod_post"]
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'نام خود را وارد کنید'}),
            "last_name": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'نام خانوادگی خود را وارد کنید'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-input', 'placeholder': '09xxxxxxxxx'}),
            "province": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'مثلا: تهران'}),
            "city": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'مثلا: تهران'}),
            "cod_post": forms.TextInput(attrs={'class': 'form-input', 'placeholder': '12345-67890'}),
            # اگر فیلد address دارید و از Textarea استفاده می‌شود:
        }

    # در صورت نیاز می‌توانید clean methods را هم اضافه کنید
