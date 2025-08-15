import json
import logging
import pytest
from django.urls import reverse
from django.contrib.gis.geos import Point


LOGGER = logging.getLogger(__name__)


@pytest.mark.django_db
def test_create_incident(api_client):
    url = reverse("incident-list")
    payload = {
        "title": "Power Outage",
        "description": "Transformer issue",
        "severity": 4,
        "location": [3.3792, 6.5244],  # lon, lat
    }
    res = api_client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert res.status_code == 201
    data = res.json()
    assert data["risk_score"] == 4.0
    assert data["status"] == "queued"


@pytest.mark.django_db
def test_filter_incident_by_bbox(api_client, incident_factory):
    inside = incident_factory(location=Point(3.38, 6.52))
    outside = incident_factory(location=Point(0.0, 0.0))
    url = reverse("incident-list") + "?bbox=3.30,6.40,3.50,6.60"
    res = api_client.get(url)
    ids = [i["id"] for i in res.json()]
    assert str(inside.id) in ids
    assert str(outside.id) not in ids
