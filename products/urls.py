from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewset, basename='product')

urlpatterns = [
    #path('categories/<int:category_id>/products/',views.CategoryProductsAPIView.as_view()),
    path('products_/',views.ProductApiView.as_view(),name='products_'),
    path('products_/<int:pk>/',views.ProductApiView.as_view(),name='products_detail'),
]
urlpatterns += router.urls
