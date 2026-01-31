from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
# local
from .models import Enrollment, Attendance, Assignment
from .serializers import EnrollmentSerializers, EnrollmenStudentSerializer, AttendanceSerializer, AssignmentSerializer
from apps.users.permissions import IsStudent, IsAdminOrIsMentor


class EnrollmentCreateAPIView(generics.CreateAPIView):
  queryset = Enrollment.objects.all()
  serializer_class = EnrollmentSerializers
  permission_classes = [IsAuthenticated, IsStudent]

  def perform_create(self, serializer):
    serializer.save(student=self.request.user)

class EnrollmentListAPIView(generics.ListAPIView):
  serializer_class = EnrollmentSerializers
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Enrollment.objects.all()
    return Enrollment.objects.filter(student=user)

class EnrollmentUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = EnrollmenStudentSerializer
  permission_classes = [IsAuthenticated, IsStudent]

  def get_queryset(self):
    return Enrollment.objects.filter(student=self.request.user)

# attendence
class AttendenceAPIView(generics.CreateAPIView):
  queryset = Attendance.objects.all()
  serializer_class = AttendanceSerializer
  permission_classes = [IsAuthenticated, IsAdminOrIsMentor]

class AttendenceListAPIView(generics.ListAPIView):
  queryset = Attendance.objects.all()
  serializer_class = AttendanceSerializer
  permission_classes = [IsAuthenticated]

class AttendenceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Attendance.objects.all()
  serializer_class = AttendanceSerializer
  permission_classes = [IsAuthenticated, IsAdminOrIsMentor]

# assignmen

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('lesson').all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['lesson', 'due_date']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminOrIsMentor()]

class AssignmentUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.select_related('lesson').all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsMentor]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "success": True,
            "message": "Assignment muvaffaqiyatli yangilandi",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        assignment_title = instance.title
        assignment_id = instance.id
        self.perform_destroy(instance)

        return Response({
            "success": True,
            "message": f"Assignment #{assignment_id} '{assignment_title}' o'chirildi"
        }, status=status.HTTP_200_OK)
