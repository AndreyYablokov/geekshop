from django.db.models import F
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import connection
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from users.models import User
from products.models import ProductCategory, Product
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm
from admins.forms import CategoryAdminCreateForm, ProductAdminCreateForm


class AdminTemplateView(TemplateView):
    template_name = 'admins/index.html'

    def get_context_data(self, **kwargs):
        context = super(AdminTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ-панель'
        return context

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(AdminTemplateView, self).dispatch(request, *args, **kwargs)


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


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'admins/admin-categories-read.html'

    def get_context_data(self, **kwargs):
        context = super(CategoriesListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Категории'
        return context

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesListView, self).dispatch(request, *args, **kwargs)


class CategoriesCreateView(CreateView):
    model = ProductCategory
    form_class = CategoryAdminCreateForm
    success_url = reverse_lazy('admins:admin_categories_read')
    template_name = 'admins/admin-categories-create.html'

    def get_context_data(self, **kwargs):
        context = super(CategoriesCreateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Создать категорию'
        return context

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesCreateView, self).dispatch(request, *args, **kwargs)


class CategoriesUpdateView(UpdateView):
    model = ProductCategory
    form_class = CategoryAdminCreateForm
    success_url = reverse_lazy('admins:admin_categories_read')
    template_name = 'admins/admin-categories-update-delete.html'

    def get_context_data(self, **kwargs):
        context = super(CategoriesUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Обновление категории'
        return context

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


class CategoriesDeleteView(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('admins:admin_categories_read')
    template_name = 'admins/admin-categories-update-delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesDeleteView, self).dispatch(request, *args, **kwargs)


class ProductsListView(ListView):
    model = Product
    template_name = 'admins/admin-products-read.html'

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Продукты'
        return context

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductsListView, self).dispatch(request, *args, **kwargs)


class ProductsCreateView(CreateView):
    model = Product
    form_class = ProductAdminCreateForm
    success_url = reverse_lazy('admins:admin_products_read')
    template_name = 'admins/admin-products-create.html'

    def get_context_data(self, **kwargs):
        context = super(ProductsCreateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Создать продукт'
        return context

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductsCreateView, self).dispatch(request, *args, **kwargs)


class ProductsUpdateView(UpdateView):
    model = Product
    form_class = ProductAdminCreateForm
    success_url = reverse_lazy('admins:admin_products_read')
    template_name = 'admins/admin-products-update-delete.html'

    def get_context_data(self, **kwargs):
        context = super(ProductsUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Обновление продукта'
        return context

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductsUpdateView, self).dispatch(request, *args, **kwargs)


class ProductsDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('admins:admin_products_read')
    template_name = 'admins/admin-products-update-delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductsDeleteView, self).dispatch(request, *args, **kwargs)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

# @user_passes_test(lambda user: user.is_staff)
# def index(request):
#     context = {'title': 'GeekShop - Админ-панель'}
#     return render(request, 'admins/index.html', context)

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
