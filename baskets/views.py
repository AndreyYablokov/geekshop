from django.shortcuts import HttpResponseRedirect

from products.models import Product
from baskets.models import Basket


def basket_add(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=user, product=product)

    if not baskets.exists():
        if product.quantity > 0:
            Basket.objects.create(user=user, product=product, quantity=1)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        basket = baskets.first()
        if basket.quantity < product.quantity:
            basket.quantity += 1
            basket.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
