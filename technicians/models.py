from django.contrib.gis.db import models


from accounts.models import User
from utils.models import BaseABCModel

# Create your models here.


class Technician(BaseABCModel, models.Model):
    user = models.OneToOneField(User, related_name="technician_profile", on_delete=models.CASCADE)

    is_available = models.BooleanField(default=True)
    phone = models.CharField(blank=True, null=True)
    location = models.PointField(geography=True)  # WGS84 coords


    def __str__(self):
        return f"{self.user.name} ({'available' if self.is_available else 'busy'})"

