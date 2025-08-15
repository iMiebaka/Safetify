from rest_framework import serializers
from django.contrib.gis.geos import Point

class PointFieldSerializer(serializers.Field):
    """Serialize a Point as [lon, lat] and deserialize back to Point."""
    def to_representation(self, value):
        return [value.x, value.y]  # x=lon, y=lat

    def to_internal_value(self, data):
        if not isinstance(data, (list, tuple)) or len(data) != 2:
            raise serializers.ValidationError(
                "Location must be a [lon, lat] array."
            )
        try:
            lon, lat = map(float, data)
            return Point(lon, lat)
        except ValueError:
            raise serializers.ValidationError("Coordinates must be numbers.")

