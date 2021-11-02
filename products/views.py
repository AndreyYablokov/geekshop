from django.shortcuts import render

from products.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView


class ProductsTemplateView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(ProductsTemplateView, self).get_context_data(**kwargs)
        context.update({
            'title': 'GeekShop',
            'header': 'GeekShop Store',
            'page_text': 'Новые образы и лучшие бренды на GeekShop Store. '
                         'Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям.',
            'button_text': 'Начать покупки',
        })
        return context


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)

        context.update({
            'title': 'GeekShop - Каталог',
            'header': 'GeekShop',
        })

        categories = [category
                      for category in ProductCategory.objects.all()
                      if Product.objects.filter(category=category)
                      ]
        context['categories'] = categories

        category_id = self.kwargs.get('category_id')
        if not self.kwargs.get('page'):
            page = 1
        else:
            page = self.kwargs['page']
        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()
        paginator = Paginator(products, 3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        context['products'] = products_paginator

        return context


# def products(request, category_id=None, page=1):
#     context = {
#         'title': 'GeekShop - Каталог',
#         'header': 'GeekShop',
#     }
#
#     categories = [category
#                   for category in ProductCategory.objects.all()
#                   if Product.objects.filter(category=category)
#                   ]
#     context['categories'] = categories
#
#     if category_id:
#         products = Product.objects.filter(category_id=category_id)
#     else:
#         products = Product.objects.all()
#     paginator = Paginator(products, 3)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#     context['products'] = products_paginator
#
#     return render(request, 'products/products.html', context)


# def index(request):
#     context = {
#         'title': 'GeekShop',
#         'header': 'GeekShop Store',
#         'page_text': 'Новые образы и лучшие бренды на GeekShop Store. '
#                      'Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям.',
#         'button_text': 'Начать покупки',
#     }
#     return render(request, 'products/index.html', context)
