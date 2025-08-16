from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Incident, Assignment
from .serializers import (
    IncidentSerializer,
    AssignmentSerializer,
)
from .filters import IncidentFilter
from technicians.services import assign_nearest_technician




class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all().order_by("-created_at")
    serializer_class = IncidentSerializer
    filterset_class = IncidentFilter

    @action(detail=True, methods=["post"], url_path="assign-nearest")
    def assign_nearest(self, request, pk=None):
        incident = self.get_object()
        radius = request.data.get("radius_m")
        radius = float(radius) if radius else None

        assignment = assign_nearest_technician(incident, radius)
        if not assignment:
            return Response(
                {
                    "status": incident.status,
                    "message": "No technician within radius; incident queued.",
                },
                status=status.HTTP_202_ACCEPTED,
            )

        return Response(AssignmentSerializer(assignment).data)



class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by("-created_at")
    serializer_class = AssignmentSerializer