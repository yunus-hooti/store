from django import forms

from .models import Category



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("این دسته بندی وحود دارد")
        return name

