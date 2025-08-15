from rest_framework import viewsets
from django.db import transaction
from django.contrib.gis.geos import Point
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.db.models.functions import Distance

from technicians.serializers import (
    CreateTechnicianSerializer,
    TechnicianSerializer,
)
from .services import DEFAULT_RADIUS_M
from technicians.models import Technician

# Create your views here.


class TechnicianViewSet(viewsets.ModelViewSet):
    queryset = Technician.objects.all().order_by("id")
    serializer_class = TechnicianSerializer

    @action(detail=False, methods=["get"], url_path="nearby")
    def nearby(self, request):
        try:
            lon = float(request.query_params.get("lon"))
            lat = float(request.query_params.get("lat"))
            radius = float(request.query_params.get("radius", DEFAULT_RADIUS_M))
        except (TypeError, ValueError):
            return Response(
                {"detail": "lon and lat query parameters are required"}, status=400
            )

        origin = Point(lon, lat, srid=4326)
        qs = (
            Technician.objects.filter(is_available=True)
            .annotate(distance=Distance("location", origin))
            .order_by("distance")
        )

        data = []
        for tech in qs:
            if tech.distance.m <= radius:
                record = self.serializer_class(tech).data
                record["distance_meters"] = float(tech.distance.m)
                data.append(record)

        return Response(data)

    @action(detail=False, methods=["post"], url_path="sign-up")
    @transaction.atomic
    def sign_up(self, request: Request):
        serializer = CreateTechnicianSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Account created"})
