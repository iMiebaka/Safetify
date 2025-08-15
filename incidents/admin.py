from django.contrib import admin

from incidents.models import Assignment, Incident

# Register your models here.
admin.site.register(Incident)
admin.site.register(Assignment)
