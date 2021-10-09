from django.shortcuts import render

import os
import json

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
    root_dir = os.path.join(os.getcwd(), 'products/fixtures')
    context_file_name = os.path.join(root_dir, 'products.json')
    with open(context_file_name, 'r', encoding='utf-8') as f:
        context = json.load(f)

    return render(request, 'products/products.html', context)
