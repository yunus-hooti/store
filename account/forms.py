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

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone.isdigit():
            if len(phone) == 11:
                if User.manager.filter(phone=phone).exists():
                    raise forms.ValidationError('این شماره قبلن ثبت نام کرده')
                return phone
            else:
                raise forms.ValidationError('شماره باید 11 رقم باشد')
        else:
            raise forms.ValidationError('شماره باید عدد باشد')


class AddressCreatedForm(forms.ModelForm):
    class Meta:
        model = AddressUser
        fields = ["first_name", "last_name", "phone_number", "province", "city", "cod_post"]
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'نام خود را وارد کنید'}),
            "last_name": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'نام خانوادگی خود را وارد کنید'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-input', 'placeholder': '09xxxxxxxxx'}),
            "province": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'مثلا: تهران'}),
            "city": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'مثلا: تهران'}),
            "cod_post": forms.TextInput(attrs={'class': 'form-input', 'placeholder': '12345-67890'}),
        }

