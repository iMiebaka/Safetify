import json
import pytest
import logging
from django.urls import reverse
from incidents.models import Incident
from django.contrib.gis.geos import Point


from technicians.serializers import CreateTechnicianSerializer

LOGGER = logging.getLogger(__name__)


@pytest.mark.django_db
def test_assign_nearest_technician(api_client):
    incident = Incident.objects.create(
        title="Leak", severity=2, location=Point(3.38, 6.52)
    )
    tech = CreateTechnicianSerializer(
        data={
            "user": {
                "first_name": "Tech",
                "username": "techa",
                "last_name": "1",
                "email": "tech1@safetify.com",
                "password": "1234",
            },
            "payload": {"location": (3.381, 6.523)},
        }
    )
    tech.is_valid(raise_exception=True)
    tech.save()
    url = reverse("incident-assign-nearest", args=[incident.id])
    res = api_client.post(url, data=json.dumps({}), content_type="application/json")
    assert res.status_code == 200
    assert res.json()["technician"]["user"] == "Tech 1"


@pytest.mark.django_db
def test_assign_when_none_available(api_client):
    incident = Incident.objects.create(title="Leak", severity=2, location=Point(0, 0))
    url = reverse("incident-assign-nearest", args=[incident.id])
    res = api_client.post(url, data=json.dumps({}), content_type="application/json")
    assert res.status_code == 202
    incident.refresh_from_db()
    assert incident.status == "queued"
