from django import forms
from orders.models import Order, OrderItem
from products.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='цена', required=False)

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.get_items().select_related()

    class Meta:
        model = OrderItem
        exclude = ()
