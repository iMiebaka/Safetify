from django_filters import rest_framework as filters
from django.contrib.gis.geos import Polygon
from .models import Incident

class IncidentFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="status")
    bbox = filters.CharFilter(method="filter_bbox")  # minLon,minLat,maxLon,maxLat

    class Meta:
        model = Incident
        fields = ["status"]

    def filter_bbox(self, queryset, name, value):
        try:
            min_lon, min_lat, max_lon, max_lat = map(float, value.split(","))
        except (ValueError, AttributeError):
            return queryset.none()

        bbox_polygon = Polygon.from_bbox((min_lon, min_lat, max_lon, max_lat))
        return queryset.filter(location__within=bbox_polygon)
