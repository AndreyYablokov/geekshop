from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from geekshop import settings
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket
from django.views import View


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
                auth.login(request, user)
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
                                          'Проверьте почту')
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
        form = UserProfileForm(instance=request.user)
        context = self.get_context_data(form, request)
        return render(request, 'users/profile.html', context)

    def post(self, request):
        form = UserProfileForm(instance=request.user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно обновлены')
            return HttpResponseRedirect(reverse('users:profile'))
        context = self.get_context_data(form, request)
        return render(request, 'users/profile.html', context)

    @staticmethod
    def get_context_data(form, request):
        context = {
            'title': 'GeekShop - Профиль',
            'form': form,
            'baskets': Basket.objects.filter(user=request.user),
        }
        return context

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)


def verify(request):
    pass

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
