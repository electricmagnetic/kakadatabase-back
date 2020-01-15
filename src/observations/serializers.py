from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField

from .models import Observation, BirdObservation
from birds.serializers import BirdSerializer


class ObservationSerializer(serializers.ModelSerializer):
    contributor = serializers.StringRelatedField(many=False)
    status = serializers.CharField(source='get_status_display')
    observation_type = serializers.CharField(
        source='get_observation_type_display'
    )

    class Meta:
        model = Observation
        exclude = ('moderator_notes', )


class BirdObservationSerializer(serializers.ModelSerializer):
    banded = serializers.CharField(source='get_banded_display')
    sex_guess = serializers.CharField(source='get_sex_guess_display')
    life_stage_guess = serializers.CharField(
        source='get_life_stage_guess_display'
    )

    bird = BirdSerializer(many=False, read_only=True)
    observation = ObservationSerializer(many=False, read_only=True)

    class Meta:
        model = BirdObservation
        fields = '__all__'

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related(
            "bird",
            "bird__band_combo",
            "bird__area",
            "bird__profile",
            "observation",
            "observation__contributor",
        )

        return queryset
