from django.urls import path

from users.views import UserLoginView, UserRegistrationView, UserLogoutView, UserProfileView, UserVerifyView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('verify/<str:email>/<str:activation_key>', UserVerifyView.as_view(), name='verify'),
]
