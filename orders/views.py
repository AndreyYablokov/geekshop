from django.shortcuts import render
from django.views.generic import ListView

from orders.models import Order


class OrdersListView(ListView):
    model = Order
    template_name = 'orders/orders-read.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
