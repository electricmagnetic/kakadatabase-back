from rest_framework import serializers

from .models import Bird


class BirdSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    sex = serializers.CharField(source='get_sex_display')
    age = serializers.ReadOnlyField(source='get_age')
    life_stage = serializers.ReadOnlyField(source='get_life_stage')

    area = serializers.StringRelatedField(many=False)
    band_combo = serializers.StringRelatedField(many=False)

    class Meta:
        model = Bird
        fields = "__all__"

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("area", "band_combo")

        return queryset
