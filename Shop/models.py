from django.db import models
from django.contrib.auth.models import User
import datetime
import os


def getFile(request, filename):
    new_file = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    new_filename = '%s%s' % (new_file, filename)
    return os.path.join('uploads/', new_filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=getFile)
    description = models.TextField(max_length=500)
    status = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to=getFile)
    description = models.TextField(max_length=500)
    quantity = models.IntegerField()
    old_price = models.FloatField()
    offer_price = models.IntegerField()
    status = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(null=True, blank=False)
    created_at = models.DateField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.product_quantity*self.product.offer_price


class Fav(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

# Create your models here.
