from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.users.permissions import IsTutorOrSuperAdmin
from apps.tasks.models import HomeworkTask, HomeworkSubmission
from apps.tasks.serializers import HomeworkTaskSerializer, HomeworkSubmissionSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        summary="List homework tasks",
        description="Retrieve a list of homework tasks. "
                    "Tutors see only tasks assigned to their groups. "
                    "SuperAdmins can see all tasks."
    ),
    retrieve=extend_schema(
        summary="Retrieve homework task",
        description="Get detailed information about a specific homework task by ID."
    ),
    create=extend_schema(
        summary="Create homework task",
        description="Create a new homework task for a group. "
                    "Tutors can create tasks only for their own groups."
    ),
    update=extend_schema(
        summary="Update homework task",
        description="Update an existing homework task."
    ),
    partial_update=extend_schema(
        summary="Partially update homework task",
        description="Update specific fields of an existing homework task."
    ),
    destroy=extend_schema(
        summary="Delete homework task",
        description="Delete a homework task from the system."
    ),
)
@extend_schema(tags=["API - Homework / Tasks"])
class HomeworkTaskViewSet(viewsets.ModelViewSet):

    serializer_class = HomeworkTaskSerializer
    permission_classes = [IsAuthenticated, IsTutorOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user
        qs = HomeworkTask.objects.select_related("group", "created_by")
        if getattr(user, "role", None) == "tutor":
            qs = qs.filter(group__tutor=user)
        return qs.order_by("-id")

    def perform_create(self, serializer):
        user = self.request.user
        group = serializer.validated_data["group"]
        if getattr(user, "role", None) == "tutor" and group.tutor_id != user.id:
            raise PermissionDenied("You can create homework only for your groups.")
        serializer.save(created_by=user)


@extend_schema_view(
    list=extend_schema(
        summary="List homework submissions",
        description="Retrieve a list of homework submissions. "
                    "Tutors see submissions from their groups only."
    ),
    retrieve=extend_schema(
        summary="Retrieve homework submission",
        description="Get detailed information about a specific submission."
    ),
    create=extend_schema(
        summary="Create homework submission",
        description="Create a submission for a homework task. "
                    "Tutors can create/accept submissions only for their groups."
    ),
    update=extend_schema(
        summary="Update homework submission",
        description="Update an existing submission."
    ),
    partial_update=extend_schema(
        summary="Partially update homework submission",
        description="Update specific fields of a submission."
    ),
    destroy=extend_schema(
        summary="Delete homework submission",
        description="Delete a submission from the system."
    ),
)
@extend_schema(tags=["API - Homework / Submissions"])
class HomeworkSubmissionViewSet(viewsets.ModelViewSet):

    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [IsAuthenticated, IsTutorOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user
        qs = HomeworkSubmission.objects.select_related(
            "homework_task", "student", "homework_task__group"
        )
        if getattr(user, "role", None) == "tutor":
            qs = qs.filter(homework_task__group__tutor=user)
        return qs.order_by("-id")

    def perform_create(self, serializer):
        user = self.request.user
        task = serializer.validated_data["homework_task"]
        if getattr(user, "role", None) == "tutor" and task.group.tutor_id != user.id:
            raise PermissionDenied(
                "You can accept/create submissions only for your groups (for now)."
            )
        serializer.save()