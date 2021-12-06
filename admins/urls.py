from django.urls import path

from admins.views import AdminTemplateView, UserCreateView, UserListView, UserUpdateView, UserDeleteView, \
    CategoriesListView, CategoriesCreateView, CategoriesUpdateView, CategoriesDeleteView, \
    ProductsListView, ProductsCreateView, ProductsUpdateView, ProductsDeleteView

app_name = 'admins'

urlpatterns = [
    path('', AdminTemplateView.as_view(), name='index'),

    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-read/', UserListView.as_view(), name='admin_users_read'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),

    path('categories-create/', CategoriesCreateView.as_view(), name='admin_categories_create'),
    path('categories-read/', CategoriesListView.as_view(), name='admin_categories_read'),
    path('categories-update/<int:pk>/', CategoriesUpdateView.as_view(), name='admin_categories_update'),
    path('categories-delete/<int:pk>/', CategoriesDeleteView.as_view(), name='admin_categories_delete'),

    path('products-create/', ProductsCreateView.as_view(), name='admin_products_create'),
    path('products-read/', ProductsListView.as_view(), name='admin_products_read'),
    path('products-update/<int:pk>/', ProductsUpdateView.as_view(), name='admin_products_update'),
    path('products-delete/<int:pk>/', ProductsDeleteView.as_view(), name='admin_products_delete'),
]
