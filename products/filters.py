from django_filters import rest_framework as filters
from .models import Products


class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Products
        fields = ['title', 'category', 'price_min', 'price_max']