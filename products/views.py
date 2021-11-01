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


def products(request, category_id=None):
    context = {
        'title': 'GeekShop - Каталог',
        'header': 'GeekShop',
    }

    categories = []
    for category in ProductCategory.objects.all():
        if Product.objects.filter(category=category):
            categories.append(category)
    context['categories'] = categories
        
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    context['products'] = products

    return render(request, 'products/products.html', context)
