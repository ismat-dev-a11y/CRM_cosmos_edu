from rest_framework import serializers
from .models import StoredFile


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StoredFile
        fields = ['id', 'file', 'file_type', 'url', 'name', 'size', 'uploaded_at']
        read_only_fields = ['url', 'name', 'uploaded_at']

    def create(self, validated_data):
        file_obj = validated_data.get('file')
        validated_data['size'] = file_obj.size
        validated_data['name'] = file_obj.name
        return super().create(validated_data)