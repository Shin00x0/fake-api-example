from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserApiViewh.as_view(),name='users'),
    path('users/<int:pk>/', views.UserApiViewh.as_view(),name='user')
]