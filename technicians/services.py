import logging
from django.contrib.gis.db.models.functions import Distance
from django.db import transaction

from technicians.models import Technician
from incidents.models import Incident, Assignment

DEFAULT_RADIUS_M = 5000  # default search radius = 5 km
LOGGER = logging.getLogger(__name__)

@transaction.atomic
def assign_nearest_technician(incident: Incident, radius_m: float | None = None) -> Assignment | None:
    """
    Finds the nearest available technician within radius_m meters,
    assigns them to the incident, and returns the Assignment.
    If none found, incident remains queued and returns None.
    """
    radius = radius_m or DEFAULT_RADIUS_M
    origin = incident.location

    # Query available technicians ordered by distance
    tech_qs = (
        Technician.objects
        .filter(is_available=True)
        .annotate(distance=Distance("location", origin))
        .order_by("distance")
    )

    
    nearest = None
    for tech in tech_qs:
        if tech.distance.m <= radius:
            nearest = tech
            break

    if not nearest:
        # No tech found in range
        incident.status = "queued"
        incident.save(update_fields=["status"])
        return None

    # Create assignment & update statuses
    assignment = Assignment.objects.create(
        incident=incident,
        technician=nearest,
        distance_meters=float(nearest.distance.m),
    )
    incident.status = "assigned"
    incident.save(update_fields=["status"])
    nearest.is_available = False
    nearest.save(update_fields=["is_available"])

    return assignment
