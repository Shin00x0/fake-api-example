from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from .serializers import ProductSerializer,CategorySerializer,ProductSerializerCreate
from .models import Products,Category

from .pagination import LargeResultsSetPagination
from django.http import Http404


from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAuthenticated


from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter


'''
Lo ideal no es usar Mixing, ni Viewset ni nada de esto porque la mayoria de las soluciones son personalizadas
y esto lo hace mas complejo ademas que el acoplamiento cerrado lleva a mas problemas en el futuro.
'''

class ProductApiView(APIView):
    #permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404
    
    def get(self, request, pk=None, format=None):
        if pk:
            product = self.get_object(pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            products = Products.objects.all()
            
            filterset = ProductFilter(request.GET, queryset=products)
            if not filterset.is_valid():
                return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
            filtered_qs = filterset.qs

            paginator = PageNumberPagination()
            paginator.page_size = 4
            result_page = paginator.paginate_queryset(filtered_qs, request)

            serializer = ProductSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data,status=status.HTTP_200_OK)

        
    def post(self,request,pk=None, format=None):
        serializer = ProductSerializerCreate(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk,format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewset(ModelViewSet):
    #permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter # ver si es necesario esta implementacion


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = Products.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Solucion Alternativa
    
# class CategoryProductsAPIView(APIView):
#     def get(self,request,category_id):
#         category = get_object_or_404(Category, pk=category_id)
#         products = Products.objects.filter(category=category)
#         serializer = ProductSerializer(products,many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
