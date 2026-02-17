from rest_framework import serializers
from .models import (
    DailyTask,
    HomeworkSubmission,
    HomeworkImage,
    HomeworkReview
)


class DailyTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyTask
        fields = "__all__"
        read_only_fields = ("assigned_by",)

class HomeworkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkImage
        fields = ["id", "image"]

class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    images = HomeworkImageSerializer(many=True, required=False)

    class Meta:
        model = HomeworkSubmission
        fields = ["id", "task", "student", "text_answer", "images"]
        read_only_fields = ("student",)

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        submission = HomeworkSubmission.objects.create(**validated_data)

        for image in images_data:
            HomeworkImage.objects.create(
                submission=submission,
                **image
            )

        return submission

class HomeworkReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeworkReview
        fields = "__all__"
        read_only_fields = ("mentor",)
