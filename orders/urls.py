from django.urls import path

from orders.views import OrdersListView, OrderCreateView, OrderUpdateView, OrderDeleteView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders_read'),
    path('order-create', OrderCreateView.as_view(), name='order_create'),
    path('order-update/<int:pk>', OrderUpdateView.as_view(), name='order_update'),
    path('order-delete/<int:pk>', OrderDeleteView.as_view(), name='order_delete'),
    path('order-read/<int:pk>', OrderDetailView.as_view(), name='order_read'),
    # path('order-forming/complete/<int:pk>', order_forming_complete, name='order_forming_complete'),

]
