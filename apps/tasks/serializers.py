from rest_framework import serializers
from .models import DailyTask

class DailyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTask
        fields = '__all__'
        
    def validate(self, attrs):
        if self.instance and attrs.get("is_completed") is False:
            raise serializers.ValidationError(
                "Completed task cannot be marked as incomplete"
            )
        return attrs
