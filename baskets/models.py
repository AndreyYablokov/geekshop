from django.db import models

from users.models import User
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.name} | Продукт {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        baskets_sum = 0
        for basket in baskets:
            baskets_sum += basket.sum()
        return baskets_sum

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        products_quantity = 0
        for basket in baskets:
            products_quantity += basket.quantity
        return products_quantity
