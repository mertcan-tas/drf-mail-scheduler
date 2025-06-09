from rest_framework import serializers
from django.utils import timezone

class ScheduleMailSerializer(serializers.Serializer):
    recipient_email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()
    scheduled_time = serializers.DateTimeField()
    
    def validate_scheduled_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("The submission time must be in the future.")
        return value