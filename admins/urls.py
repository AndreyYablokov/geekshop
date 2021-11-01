from django.urls import path

from admins.views import AdminTemplateView, UserCreateView, UserListView, UserUpdateView, UserDeleteView

app_name = 'admins'

urlpatterns = [
    path('', AdminTemplateView.as_view(), name='index'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-read/', UserListView.as_view(), name='admin_users_read'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
]
