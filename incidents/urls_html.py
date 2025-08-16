from django.urls import path
from django.views.generic import TemplateView

app_name = "incident_web"

urlpatterns = [
    path("", TemplateView.as_view(template_name="incidents/index.html"), name="incident_index"),
    path("i/<incident>", TemplateView.as_view(template_name="incidents/incident.html"), name="incident_single"),
    path("a/<assignment>", TemplateView.as_view(template_name="incidents/assignment.html"), name="assignment_single"),
]
