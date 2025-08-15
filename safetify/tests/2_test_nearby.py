import logging
import pytest
from django.urls import reverse

from technicians.serializers import CreateTechnicianSerializer

LOGGER = logging.getLogger(__name__)


@pytest.mark.django_db
def test_nearby_technicians(api_client):
    tech = CreateTechnicianSerializer(
        data={
            "user": {
                "password": "1234",
                "last_name": "Near",
                "first_name": "Tech",
                "username": "techNear",
                "phone": "+234083000002",
                "email": "technear@safetify.com",
            },
            "payload": {"location": (3.381, 6.523)},
        }
    )
    tech.is_valid(raise_exception=True)
    tech.save()
    tech = CreateTechnicianSerializer(
        data={
            "user": {
                "last_name": "Far",
                "password": "1234",
                "first_name": "Tech",
                "username": "techFar",
                "phone": "+234083000002",
                "email": "techfar@safetify.com",
            },
            "payload": {"location": (3.381, 6.523)},
        }
    )
    tech.is_valid(raise_exception=True)
    tech.save()
    url = reverse("technician-nearby") + "?lon=3.3792&lat=6.5244&radius=5000"
    res = api_client.get(url)
    data = res.json()
    assert any(t["user"] == "Tech Near" for t in data)
    assert all("distance_meters" in t for t in data)
