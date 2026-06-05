from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import logout, login

from .models import User, AddressUser
from .forms import CreateUserForm, AddressCreatedForm
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


# Create your views here.

def log_out(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            logout(request)
            return redirect('account:login')
        return render(request, 'account/logout.html')
    messages.success(request, "شما وارد نشدید")
    return redirect("account:login")


class RegisterView(UserPassesTestMixin, generic.FormView):
    form_class = CreateUserForm
    template_name = 'registration/register.html'

    def get_success_url(self):
        return reverse("account:register")

    def test_func(self):
        if not self.request.user.is_authenticated:
            return redirect("account:login")
        else:
            return not self.request.user.is_authenticated

    def form_invalid(self, form):
        messages.error(self.request,f"{form.errors}")
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.manager.create(
                phone=form.cleaned_data["phone"],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'], )
            user.set_password(form.cleaned_data['password_confirm'])
            user.save()
            login(self.request, user)
            return redirect("catalog:product_list")

        return self.form_invalid(form)


class ProfileView(UserPassesTestMixin, generic.TemplateView):
    template_name = 'account/profile.html'

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return True

    def handle_no_permission(self):
        return redirect("account:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_user'] = AddressUser.objects.filter(user=self.request.user)
        return context


class AddressCreatedView(UserPassesTestMixin, generic.FormView):
    template_name = "account/address_create.html"
    form_class = AddressCreatedForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = AddressUser.objects.create(user=request.user, phone_number=cd['phone_number'],
                                              first_name=cd['first_name'], last_name=cd['last_name'],
                                              province=cd['province'], city=cd['city'],
                                              cod_post=cd['cod_post'])
            user.save()
            messages.success(request, "آدرس حدید ثبت شد", extra_tags='ok_address')
            return redirect("account:profile")
        messages.success(request, 'مشکل در آدرس ارسالی')
        return redirect("account:address_create")

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return True


class DeleteAddressView(UserPassesTestMixin, generic.DeleteView):
    model = AddressUser
    template_name = "account/addressuser_confirm_delete.html"
    context_object_name = "address"

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return True

    def get_success_url(self):
        return reverse('account:profile')


class EditAddressView(UserPassesTestMixin, generic.UpdateView):
    model = AddressUser
    form_class = AddressCreatedForm
    template_name = "account/address_create.html"

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def get_success_url(self):
        return reverse('account:profile')
