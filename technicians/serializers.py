from rest_framework import serializers

from django.contrib.gis.geos import Point
from accounts.models import User
from accounts.serializers import UserSerializer
from utils.serializers import PointFieldSerializer

from .models import Technician


class TechnicianSerializer(serializers.ModelSerializer):
    location = PointFieldSerializer()

    class Meta:
        model = Technician
        fields = [
            "id",
            "user",
            "phone",
            "location",
            "is_available",
        ]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        user = User.objects.get(id=context["user"])
        context["user"] = user.name
        return context


class CreateTechnicianSerializer(serializers.Serializer):
    user = serializers.DictField()
    payload = serializers.DictField()

    class Meta:
        model = Technician

    def create(self, validated_data):
        user = UserSerializer(data=validated_data["user"])
        user.is_valid(raise_exception=True)
        user.save()

        payload = validated_data["payload"]
        t = Technician.objects.get_or_create(
            user_id=user.data["id"],
            defaults={
                "location": Point(payload["location"][0], payload["location"][1])
            },
        )
        return t[0]
