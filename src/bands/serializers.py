from rest_framework import serializers

from .models import BandCombo

from birds.serializers import BaseBirdSerializer
from birds.models import Bird


class BandComboSerializer(serializers.ModelSerializer):
    bird = BaseBirdSerializer(many=False, read_only=True)

    class Meta:
        model = BandCombo
        fields = (
            'combo',
            'bird',
        )
