from django.urls import path

from orders.views import OrdersListView
# from users.views import UserLoginView, UserRegistrationView, UserLogoutView, UserProfileView, UserVerifyView

app_name = 'orders'

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders_read'),
    # path('', OrdersView.as_view(), name='orders'),
    # path('order-forming/complete/<int:pk>', order_forming_complete, name='order_forming_complete'),
    # path('order-create', OrderCreateView.as_view(), name='order_create'),
    # path('order-read/<int:pk>', OrderReadView.as_view(), name='order_read'),
    # path('order-update/<int:pk>', OrderUpdateView.as_view(), name='order_update'),
    # path('order-delete/<int:pk>', OrderDeleteView.as_view(), name='order_delete'),
]