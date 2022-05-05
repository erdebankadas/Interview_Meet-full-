from rest_framework import serializers
from quiz.serializer_fields import JsonListField
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    data = JsonListField()
    score = JsonListField()

    class Meta:
        model = Game
        fields = ['name', 'user', 'data', 'score', 'started_at', 'updated_at']


