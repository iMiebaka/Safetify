from rest_framework import serializers

from .models import Incident, Assignment


class IncidentSerializer(serializers.ModelSerializer):
    from utils.serializers import PointFieldSerializer

    location = PointFieldSerializer()

    class Meta:
        model = Incident
        fields = [
            "id",
            "title",
            "status",
            "severity",
            "location",
            "created_at",
            "assignment",
            "risk_score",
            "updated_at",
            "description",
        ]
        read_only_fields = [
            "status",
            "risk_score",
            "assignment",
            "created_at",
            "updated_at",
        ]


class AssignmentSerializer(serializers.ModelSerializer):
    from technicians.serializers import TechnicianSerializer

    incident = IncidentSerializer(read_only=True)
    technician = TechnicianSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ["incident", "technician", "distance_meters", "assigned_at"]
