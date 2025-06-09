from rest_framework import serializers

class AbstractSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)