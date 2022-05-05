from rest_framework import serializers
from quiz.serializer_fields import JsonListField
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    extra_fields = JsonListField()

    class Meta:
        model = Job
        fields = '__all__'