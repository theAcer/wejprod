from django.urls import path, include
from users.models import CustomUser
from rest_framework import serializers

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_staff', 'id']