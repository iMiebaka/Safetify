from django.contrib.gis.db import models
from django.utils import timezone

class Incident(models.Model):
    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("assigned", "Assigned"),
        ("resolved", "Resolved"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    severity = models.PositiveSmallIntegerField(default=1)  # 1–5
    risk_score = models.FloatField(default=0)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="queued")
    location = models.PointField(geography=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.risk_score:
            # Simple placeholder risk score = severity for now
            self.risk_score = float(self.severity)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Incident #{self.id}: {self.title} [{self.status}]"


class Assignment(models.Model):
    incident = models.OneToOneField(
        Incident, on_delete=models.CASCADE, related_name="assignment"
    )
    technician = models.ForeignKey(
        "technicians.Technician", on_delete=models.PROTECT, related_name="assignments"
    )
    distance_meters = models.FloatField()
    assigned_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Incident #{self.incident_id} → {self.technician.name}"
