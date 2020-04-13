from .models import Match, Player
from rest_framework import serializers
import json

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = [
            'steam_id',
            'name',
            'rating',
            'color',
            'civ'
        ]


# create class to serializer model
class MatchSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Match
        fields = [
            'name',
            'match_date',
            'match_played',
            'players'
        ]
    def __str__(self):
        return json.dumps(self)

    def create(self, validated_data):
        player_validated_data = validated_data.pop('players')
        match = Match.objects.create(**validated_data)
        player_set_serializer = self.fields['players']
        for each in player_validated_data:
            each['match'] = match
        player_set_serializer.create(player_validated_data)
        return match
