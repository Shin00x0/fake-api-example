from rest_framework import serializers
from .models import Products,Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializerCreate(serializers.ModelSerializer):    
    class Meta:
        model = Products
        fields = ['id','title','description','price','category','image']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Products
        fields = ['id','title','description','price','category','image']

