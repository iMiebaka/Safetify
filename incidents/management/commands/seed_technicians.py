from django.db import transaction
from django.core.management.base import BaseCommand
from technicians.serializers import CreateTechnicianSerializer


class Command(BaseCommand):
    help = "Seed sample technicians into the database"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        tech_coords = [
            {
                "user": {
                    "last_name": "A",
                    "password": "1234",
                    "username": "techa",
                    "first_name": "Tech",
                    "phone": "+234083000000",
                    "email": "techa@safetify.com",
                },
                "payload": {
                    "location": (3.3792, 6.5244)  # Lagos
                },
            },
            {
                "user": {
                    "last_name": "B",
                    "password": "1234",
                    "first_name": "Tech",
                    "username": "techb",
                    "phone": "+234083000001",
                    "email": "techb@safetify.com",
                },
                "payload": {"location": (3.40, 6.50)},
            },
            {
                "user": {
                    "last_name": "C",
                    "password": "1234",
                    "first_name": "Tech",
                    "username": "techc",
                    "phone": "+234083000002",
                    "email": "techc@safetify.com",
                },
                "payload": {"location": (3.30, 6.55)},
            },
        ]
        for tech_coord in tech_coords:
            serializer = CreateTechnicianSerializer(data=tech_coord)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        self.stdout.write(self.style.SUCCESS("Technicians seeded successfully 🌱"))
