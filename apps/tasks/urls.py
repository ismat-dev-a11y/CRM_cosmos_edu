from rest_framework.routers import DefaultRouter
from apps.tasks.views import HomeworkTaskViewSet, HomeworkSubmissionViewSet

router = DefaultRouter()
router.register(r"homework/tasks", HomeworkTaskViewSet, basename="homework-tasks")
router.register(r"homework/submissions", HomeworkSubmissionViewSet, basename="homework-submissions")

urlpatterns = router.urls
