from django import forms

from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User
from products.models import ProductCategory, Product


class UserAdminRegistrationForm(UserRegistrationForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'age', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4'}))


class CategoryAdminCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    discount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control py-4'}),
                                  required=False, min_value=-90, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        exclude = ()


class ProductAdminCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control py-4'}))
    price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control py-4'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control py-4'}))

    class Meta:
        model = Product
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ProductAdminCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'custom-select'
