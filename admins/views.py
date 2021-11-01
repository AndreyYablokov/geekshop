from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


@user_passes_test(lambda user: user.is_staff)
def index(request):
    context = {'title': 'GeekShop - Админ-панель'}
    return render(request, 'admins/index.html', context)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Пользователи'
        return context

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users_read')
    template_name = 'admins/admin-users-create.html'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Создать пользователя'
        return context

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users_read')
    template_name = 'admins/admin-users-update-delete.html'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Обновление пользователя'
        return context

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('admins:admin_users_read')
    template_name = 'admins/admin-users-update-delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.safe_delete()
        return HttpResponseRedirect(success_url)

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda user: user.is_staff)
# def admin_users_read(request):
#     context = {
#         'title': 'GeekShop - Пользователи',
#         'users': User.objects.all(),
#     }
#     return render(request, 'admins/admin-users-read.html', context)


# @user_passes_test(lambda user: user.is_staff)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users_read'))
#     else:
#         form = UserAdminRegistrationForm
#
#     context = {
#         'title': 'GeekShop - Создать пользователя',
#         'form': form,
#     }
#     return render(request, 'admins/admin-users-create.html', context)

# @user_passes_test(lambda user: user.is_staff)
# def admin_users_update(request, user_id):
#     user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(instance=user, files=request.FILES, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users_read'))
#     else:
#         form = UserAdminProfileForm(instance=user)
#
#     context = {
#         'title': 'GeekShop - Обновление пользователя',
#         'form': form,
#         'user': user,
#     }
#     return render(request, 'admins/admin-users-update-delete.html', context)

# @user_passes_test(lambda user: user.is_staff)
# def admin_users_delete(request, user_id):
#     user = User.objects.get(id=user_id)
#     user.safe_delete()
#     return HttpResponseRedirect(reverse('admins:admin_users_read'))
