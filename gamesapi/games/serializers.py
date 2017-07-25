from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    """use ModelSerializer class to eliminate code"""
    class Meta:
        model = Game
        fields = ('id',
                  'name',
                  'release_date',
                  'game_category',
                  'played')





