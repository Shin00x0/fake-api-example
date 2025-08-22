from rest_framework.serializers import ModelSerializer
from .models import UserModel


class UserModelSearializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "email",
            "password",
            "username",
            "role",
            "avatar",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True} 
        }