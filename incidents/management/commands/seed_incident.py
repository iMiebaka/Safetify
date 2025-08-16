from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from incidents.models import Incident


class Command(BaseCommand):
    help = "Seed sample incidents into the database"

    def handle(self, *args, **kwargs):
        incidents = [
            {
                "title": "Water Pipe Leak",
                "description": "Major pipe burst causing flooding on Broad Street",
                "severity": 3,
                "location": Point(3.3792, 6.5244),  # Lagos Island
            },
            {
                "title": "Traffic Light Outage",
                "description": "Malfunctioning traffic light at busy intersection",
                "severity": 2,
                "location": Point(3.3486, 6.6018),  # Ikeja
            },
            {
                "title": "Pothole Report",
                "description": "Large pothole causing vehicle damage on Eko Bridge",
                "severity": 2,
                "location": Point(3.3964, 6.4589),  # Near Eko Bridge
            },
            {
                "title": "Power Outage",
                "description": "Transformer failure affecting 20 buildings",
                "severity": 4,
                "location": Point(3.4231, 6.4532),  # Victoria Island
            },
            {
                "title": "Illegal Dumping",
                "description": "Construction waste dumped in residential area",
                "severity": 1,
                "location": Point(3.2857, 6.5534),  # Agege
            },
            {
                "title": "Streetlight Repair",
                "description": "Non-functional streetlight for 2 weeks",
                "severity": 2,
                "location": Point(3.4012, 6.4976),  # Surulere
            },
            {
                "title": "Flood Alert",
                "description": "Drainage blockage causing water accumulation",
                "severity": 3,
                "location": Point(3.3678, 6.5123),  # Apapa
            },
        ]

        # Create all incidents
        for incident in incidents:
            Incident.objects.create(**incident)
        self.stdout.write(self.style.SUCCESS("Incidents seeded successfully 🌱"))
