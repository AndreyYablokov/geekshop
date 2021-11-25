from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction

from geekshop import settings
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserAdditionalProfileForm
from baskets.models import Basket
from django.views import View

from users.models import User


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        context = self.get_context_data(form)
        return render(request, 'users/login.html', context)

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse('index'))
        context = self.get_context_data(form)
        return render(request, 'users/login.html', context)

    @staticmethod
    def get_context_data(form):
        context = {
            'title': 'GeekShop - Авторизация',
            'form': form,
        }
        return context


class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm
        context = self.get_context_data(form)
        return render(request, 'users/registration.html', context)

    def post(self, request):
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_mail(user):
                messages.success(request, 'Сообщение с ссылкой для подтвеждения почтового адреса отправлено. '
                                          'Проверьте почту. Ссылка действует 48 часов')
                return HttpResponseRedirect(reverse('users:login'))
            else:
                messages.success(request, 'Ошибка отправки сообщения с ссылкой для подтвеждения почтового адреса. '
                                          'Попробуйте зарегистрироваться позже')
                return HttpResponseRedirect(reverse('users:login'))
        context = self.get_context_data(form)
        return render(request, 'users/registration.html', context)

    @staticmethod
    def get_context_data(form):
        context = {
            'title': 'GeekShop - Регистрация',
            'form': form,
        }
        return context

    @staticmethod
    def send_verify_mail(user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])

        title = f'Подтверждение учетной записи {user.username}'

        message = f'Для подтверждения учетной записи {user.username} на портале \
                    {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


class UserLogoutView(View):
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('index'))


class UserProfileView(View):
    def get(self, request):
        profile_form = UserProfileForm(instance=request.user)
        additional_profile_form = UserAdditionalProfileForm(instance=request.user.userprofile)
        context = self.get_context_data(profile_form, additional_profile_form, request)
        return render(request, 'users/profile.html', context)

    @transaction.atomic
    def post(self, request):
        profile_form = UserProfileForm(instance=request.user, files=request.FILES, data=request.POST)
        additional_profile_form = UserAdditionalProfileForm(instance=request.user.userprofile, data=request.POST)
        if profile_form.is_valid() and additional_profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Данные успешно обновлены')
            return HttpResponseRedirect(reverse('users:profile'))
        context = self.get_context_data(profile_form, additional_profile_form, request)
        return render(request, 'users/profile.html', context)

    @staticmethod
    def get_context_data(profile_form, additional_profile_form, request):
        context = {
            'title': 'GeekShop - Профиль',
            'profile_form': profile_form,
            'additional_profile_form': additional_profile_form,
        }
        return context

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)


class UserVerifyView(View):
    def get(self, request, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user.activation_key == activation_key and not user.is_activation_key_expired():
                user.is_active = True
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Вы успешно зарегистрированы!')
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.success(request, 'Активация не пройедена: время действия ссылки истекло или неверный код '
                                          'активации.')
                return HttpResponseRedirect(reverse('index'))
        except Exception as e:
            messages.success(request, f'Ошибка при активации: {e.args}')
            return HttpResponseRedirect(reverse('index'))

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'title': 'GeekShop - Авторизация',
#         'form': form,
#     }
#     return render(request, 'users/login.html', context)


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#
#     context = {
#         'title': 'GeekShop - Регистрация',
#         'form': form,
#     }
#     return render(request, 'users/registration.html', context)


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserProfileForm(instance=user, files=request.FILES, data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Данные успешно обновлены')
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=user)
#     context = {
#         'title': 'GeekShop - Профиль',
#         'form': form,
#         'baskets': Basket.objects.filter(user=user),
#     }
#     return render(request, 'users/profile.html', context)

# def verify(request, email, activation_key):
#     try:
#         user = User.objects.get(email=email)
#         if user.activation_key == activation_key and not user.is_activation_key_expired():
#             user.is_active = True
#             user.save()
#             auth.login(request, user)
#             messages.success(request, 'Вы успешно зарегистрированы!')
#             return HttpResponseRedirect(reverse('index'))
#         else:
#             messages.success(request, 'Активация не пройедена: время действия ссылки истекло или неверный код '
#                                       'активации.')
#             return HttpResponseRedirect(reverse('index'))
#     except Exception as e:
#         messages.success(request, f'Ошибка при активации: {e.args}')
#         return HttpResponseRedirect(reverse('index'))
