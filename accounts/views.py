from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.pagination import PageNumberPagination
from .models import UserModel
from .serializers import UserModelSearializer

from django.shortcuts import get_object_or_404

# Create your views here.
class UserApiViewh(APIView):
    def get(self,request,pk=None):
        if pk:
            user = get_object_or_404(UserModel,pk=pk)
            serializer = UserModelSearializer(user)
        else:
            users = UserModel.objects.all()

            pagination = PageNumberPagination()
            pagination.page_size = 4
            result_page = pagination.paginate_queryset(users, request)

            serializer = UserModelSearializer(result_page, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
