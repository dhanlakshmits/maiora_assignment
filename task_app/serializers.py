from rest_framework import serializers

class GetTaskSerializer(serializers.Serializer):

    task_name = serializers.CharField(required=True)
    task_duration = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    task_start_date = serializers.CharField(required=False)
    task_end_date = serializers.CharField(required=False)


class GetCompanySerializer(serializers.Serializer):

    company_id = serializers.CharField(required=True)
    company_name = serializers.CharField(required=False)
    email_id = serializers.CharField(required=False)
    company_code = serializers.CharField(required=False)
    strength = serializers.IntegerField(required=False)
    website = serializers.CharField(required=False)
