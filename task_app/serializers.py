from rest_framework import serializers

class GetTaskSerializer(serializers.Serializer):

    task_name = serializers.CharField(required=True)
    task_duration = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    task_start_date = serializers.CharField(required=False)
    task_end_date = serializers.CharField(required=False)