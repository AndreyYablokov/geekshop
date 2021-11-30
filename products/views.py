from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse

from products.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from django.conf import settings
from django.core.cache import cache


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

    @staticmethod
    def get_categories():
        if settings.LOW_CACHE:
            key = 'categories'
            categories = cache.get(key)
            if categories is None:
                categories = [category
                              for category in ProductCategory.objects.all()
                              if Product.objects.filter(category=category)
                              ]
                cache.set(key, categories)
            return categories
        else:
            return [category
                    for category in ProductCategory.objects.all()
                    if Product.objects.filter(category=category)
                    ]

    @staticmethod
    def get_products_category(category_id):
        if settings.LOW_CACHE:
            key = f'products_category_{category_id}'
            products = cache.get(key)
            if products is None:
                products = Product.objects.filter(category_id=category_id)
                cache.set(key, products)
            return products
        else:
            return Product.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)

        context.update({
            'title': 'GeekShop - Каталог',
            'header': 'GeekShop',
        })

        context['categories'] = self.get_categories()

        category_id = self.kwargs.get('category_id')
        if not self.kwargs.get('page'):
            page = 1
        else:
            page = self.kwargs['page']
        if category_id:
            products = self.get_products_category(category_id)
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


def products_ajax(request, category_id=None, page=1):
    if request.is_ajax():
        context = {
            'title': 'GeekShop - Каталог',
            'header': 'GeekShop',
        }

        categories = [category
                      for category in ProductCategory.objects.all()
                      if Product.objects.filter(category=category)
                      ]
        context['categories'] = categories

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

        result = render_to_string(
            'products/products.html',
            context=context,
            request=request)
    else:
        result = None

    return JsonResponse({'result': result})

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
