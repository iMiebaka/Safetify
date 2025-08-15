import pytest
from rest_framework.test import APIClient
from django.contrib.gis.geos import Point

from incidents.models import Incident

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def incident_factory():
    def make(**kwargs):
        defaults = {
            "title": "Test Incident",
            "severity": 3,
            "location": Point(3.3792, 6.5244),
        }
        defaults.update(kwargs)
        return Incident.objects.create(**defaults)
    return make
