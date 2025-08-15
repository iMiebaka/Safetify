from django.urls import path
from django.views.generic import TemplateView

app_name = "incident_web"

urlpatterns = [
    path("", TemplateView.as_view(template_name="incidents/index.html"), name="incident_index"),
]
