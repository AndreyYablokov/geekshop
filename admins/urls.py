from django.urls import path

from admins.views import index, admin_users_create, admin_users_read, admin_users_update, admin_users_delete

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users-create/', admin_users_create, name='admin_users_create'),
    path('users-read/', admin_users_read, name='admin_users_read'),
    path('users-update/', admin_users_update, name='admin_users_update'),
    path('users-delete/', admin_users_delete, name='admin_users_delete'),
]
