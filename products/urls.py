from django.urls import path
from django.views.decorators.cache import cache_page

from products.views import ProductsListView, products_ajax

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='page'),
    path('<int:category_id>/ajax/', cache_page(60)(products_ajax)),
]
