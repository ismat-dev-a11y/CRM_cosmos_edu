from rest_framework import generics, status, response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

# local
from .models import Enrollment, Attendance, Assignment
from .serializers import (
    EnrollmentSerializers,
    EnrollmenStudentSerializer,
    AttendanceSerializer,
    AssignmentSerializer,
)
from apps.users.permissions import IsStudent, IsAdminOrIsMentor


@extend_schema(tags=["Enrollments"])
class EnrollmentCreateAPIView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializers
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


@extend_schema(tags=["Enrollments"])
class EnrollmentListAPIView(generics.ListAPIView):
    serializer_class = EnrollmentSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student=user)


@extend_schema(tags=["Enrollments"])
class EnrollmentUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EnrollmenStudentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)


# attendence
@extend_schema(tags=["Attendence"])
class AttendenceAPIView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsMentor]


@extend_schema(tags=["Attendence"])
class AttendenceListAPIView(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Attendance"],
    request=AttendanceSerializer,
    responses=AttendanceSerializer,
)
@api_view(['PUT'])
def updateattendence(requests, pk):
    attendence = get_object_or_404(Attendance, pk=pk)
    serializer = AttendanceSerializer(attendence, data=requests.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return response.Response(serializer.data)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# assignment


@extend_schema(tags=["Assignment"])
class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all().order_by("-created_at")
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]