from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from incidents.models import Technician

class Command(BaseCommand):
    help = "Seed sample technicians into the database"

    def handle(self, *args, **kwargs):
        tech_coords = [
            ("Tech A", (3.3792, 6.5244)),  # Lagos
            ("Tech B", (3.40, 6.50)),
            ("Tech C", (3.30, 6.55)),
        ]
        for name, (lon, lat) in tech_coords:
            Technician.objects.get_or_create(
                name=name,
                defaults={"location": Point(lon, lat)},
            )
        self.stdout.write(self.style.SUCCESS("Technicians seeded successfully"))
