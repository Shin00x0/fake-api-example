from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20)
    image = models.URLField()

    def __str__(self):
        return self.name

class Products(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=4, decimal_places=1)
    description = models.TextField()
    category = models.ForeignKey(Category, models.CASCADE)

    def __str__(self):
        return self.title

class Image(models.Model):
    product = models.ForeignKey(Products,related_name='image',on_delete=models.CASCADE)
    image = models.URLField()

    def __str__(self):
        return self.product.title 