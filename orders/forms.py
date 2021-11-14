from django import forms
from orders.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()
