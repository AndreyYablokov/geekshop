from django.db.models import F
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from products.models import Product
from baskets.models import Basket


@login_required
def basket_add(request, product_id):
    if request.is_ajax():
        user = request.user
        product = Product.objects.get(id=product_id)
        baskets = Basket.objects.filter(user=user, product=product)

        if not baskets.exists():
            if product.quantity > 0:
                Basket.objects.create(user=user, product=product, quantity=1)
            return JsonResponse({'result': 'success'})
        else:
            basket = baskets.first()
            if basket.quantity < product.quantity:
                basket.quantity = F('quantity') + 1
                basket.save()
            return JsonResponse({'result': 'success'})


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove_ajax(request, product_id):
    if request.is_ajax():
        product = Product.objects.get(id=product_id)
        baskets = Basket.objects.filter(user=request.user, product=product)
        for basket in baskets:
            basket.delete()
        return JsonResponse({'result': 'success'})


def basket_edit(request, basket_id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=basket_id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
    result = render_to_string('baskets/baskets.html', request=request)
    return JsonResponse({'result': result})

