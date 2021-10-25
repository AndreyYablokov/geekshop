from django.urls import path

from baskets.views import basket_add, basket_remove, basket_edit, basket_remove_ajax

app_name = 'baskets'

urlpatterns = [
    path('add/<int:product_id>/', basket_add, name='basket_add'),
    path('remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('remove_ajax/<int:product_id>/', basket_remove_ajax, name='basket_remove_ajax'),
    path('edit/<int:basket_id>/<int:quantity>/', basket_edit, name='basket_edit'),
]
