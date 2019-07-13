from rest_framework import serializers
from .models import Votes


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = ('id', 'subject', 'vote_taken', 'ayes', 'nays')
