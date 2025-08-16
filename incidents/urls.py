from rest_framework.routers import DefaultRouter
from .views import  IncidentViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r"incidents", IncidentViewSet, basename="incident")
router.register(r"assignments", AssignmentViewSet, basename="assignments")

urlpatterns = router.urls
