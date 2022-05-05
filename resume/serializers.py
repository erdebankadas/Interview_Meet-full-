from rest_framework import serializers
from quiz.serializer_fields import JsonListField
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    data = JsonListField()

    class Meta:
        model = Resume
        fields = ['data']

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        resume = Resume.objects.create(**validated_data, user=user)
        return resume
    
    def update(self, instance, validated_data):
        instance.data = validated_data.get('data', instance.data)
        instance.save()
        return instance