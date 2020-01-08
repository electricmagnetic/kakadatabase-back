from rest_framework import serializers

from .models import Bird

class BirdSerializer(serializers.ModelSerializer):
    area = serializers.StringRelatedField(many=False)
    band_combo = serializers.StringRelatedField(many=False)

    class Meta:
        model = Bird
        fields = "__all__"

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("area")

        return queryset
