from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from .models import User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'role', 'bio')