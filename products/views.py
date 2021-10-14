from django.shortcuts import render

from products.models import ProductCategory, Product

# Create your views here.


def index(request):
    context = {
        'title': 'GeekShop',
        'header': 'GeekShop Store',
        'page_text': 'Новые образы и лучшие бренды на GeekShop Store. '
                     'Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям.',
        'button_text': 'Начать покупки',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'GeekShop - Каталог',
        'header': 'GeekShop',
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all(),
    }

    return render(request, 'products/products.html', context)
