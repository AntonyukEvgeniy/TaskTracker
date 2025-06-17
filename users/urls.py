from rest_framework.routers import DefaultRouter
from users.views import EmployeeViewSet

router = DefaultRouter()
router.register("employees", EmployeeViewSet)
urlpatterns = router.urls
