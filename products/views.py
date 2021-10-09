from django.shortcuts import render


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
        'categories': ['новинки', 'одежда', 'обувь', 'аксессуары', 'подарки'],
        'products': [
            {'image_path': '/static/vendor/img/products/Adidas-hoodie.png',
             'title': 'Худи черного цвета с монограммами adidas Originals',
             'price': '6 090,00',
             'text': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни',
             },
            {'image_path': '/static/vendor/img/products/Blue-jacket-The-North-Face.png',
             'title': 'Синяя куртка The North Face',
             'price': '23 725,00',
             'text': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.',
             },
            {'image_path': '/static/vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png',
             'title': 'Коричневый спортивный oversized-топ ASOS DESIGN',
             'price': '3 390,00',
             'text': 'Материал с плюшевой текстурой. Удобный и мягкий.',
             },
            {'image_path': '/static/vendor/img/products/Black-Nike-Heritage-backpack.png',
             'title': 'Черный рюкзак Nike Heritage',
             'price': '2 340,00',
             'text': 'Плотная ткань. Легкий материал.',
             },
            {'image_path': '/static/vendor/img/products/Black-Dr-Martens-shoes.png',
             'title': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
             'price': '13 590,00',
             'text': 'Гладкий кожаный верх. Натуральный материал.',
             },
            {'image_path': '/static/vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png',
             'title': 'Темно-синие широкие строгие брюки ASOS DESIGN',
             'price': '2 890,00',
             'text': 'Легкая эластичная ткань сирсакер Фактурная ткань.',
             },
        ],
    }
    return render(request, 'products/products.html', context)
