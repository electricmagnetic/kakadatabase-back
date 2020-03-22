from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import Bird, BirdProfile


class BirdProfileSerializer(serializers.ModelSerializer):
    picture = VersatileImageFieldSerializer(sizes='profile_picture')

    class Meta:
        model = BirdProfile
        exclude = (
            'is_extended',
            'picture_ppoi',
        )


class BaseBirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bird
        fields = (
            'id',
            'slug',
            'name',
            'primary_band',
        )


class BirdSerializer(BaseBirdSerializer):
    label = serializers.CharField(source='get_label')
    status = serializers.CharField(source='get_status_display')
    sex = serializers.CharField(source='get_sex_display')
    age = serializers.ReadOnlyField(source='get_age')
    life_stage = serializers.ReadOnlyField(source='get_life_stage')

    profile = BirdProfileSerializer()

    area = serializers.StringRelatedField(many=False)
    band_combo = serializers.StringRelatedField(many=False)

    class Meta:
        model = Bird
        exclude = (
            'date_created',
            'date_modified',
        )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('area', 'band_combo', 'profile')

        return queryset
