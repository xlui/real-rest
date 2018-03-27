from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializers's fields with the model fields."""
        model = User
        fields = ('id', 'username', 'password')
        read_only_fields = ('id',)
