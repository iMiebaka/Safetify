from uuid import uuid4
from rest_framework import serializers

from accounts.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name", "username", "password", "last_name", "email"]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "password": {"required": True},
        }

    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data:dict):
        """Create and return a new user."""
        password = validated_data.pop("password")
        user = User(
            **validated_data,
            private_id=str(uuid4()),
        )
        user.set_password(password)
        user.save()
        return user
