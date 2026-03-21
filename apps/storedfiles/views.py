# apps/storedfiles/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import StoredFile
from .serializers import FileUploadSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file'     : {'type': 'string', 'format': 'binary'},
                    'file_type': {'type': 'string', 'enum': ['IMAGE', 'DOCUMENT', 'VIDEO']},
                }
            }
        },
        responses={201: FileUploadSerializer}
    )
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            stored_file = serializer.save()
            return Response({
                "id"  : stored_file.id,
                "url" : stored_file.url,
                "name": stored_file.name,
                "size": stored_file.size,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            file = StoredFile.objects.get(pk=pk)
            file.file.delete()   # MinIO dan o'chirish
            file.delete()        # DB dan o'chirish
            return Response({"message": "File o'chirildi."}, status=status.HTTP_204_NO_CONTENT)
        except StoredFile.DoesNotExist:
            return Response({"error": "File topilmadi."}, status=status.HTTP_404_NOT_FOUND)