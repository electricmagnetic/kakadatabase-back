from rest_framework import serializers

from observations.models import Contributor, Observation, BirdObservation


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'


class BirdObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirdObservation
        exclude = (
            'bird',
            'observation',
            'revisit',
        )


class ReportObservationSerializer(serializers.ModelSerializer):
    contributor = ContributorSerializer(many=False)
    challenge = serializers.CharField(allow_blank=True, required=False)

    birds = BirdObservationSerializer(many=True)

    class Meta:
        model = Observation
        exclude = (
            'status',
            'geocode',
            'region',
            'moderator_notes',
            'favourite',
            'confirmed',
        )

    def validate(self, data):
        """ Basic check to deter spam submissions """
        if data.pop('challenge', None) != 'kaka':
            raise serializers.ValidationError('Invalid submission')
        return data

    def create(self, validated_data):
        # Process Contributor, pop 'birds' before creating Observation
        contributor_data = validated_data.pop('contributor')
        contributor = Contributor.objects.create(**contributor_data)
        birds_data = validated_data.pop('birds')

        # Save Observation
        observation = Observation.objects.create(
            contributor=contributor, **validated_data
        )

        # Process BirdObservations
        for bird_data in birds_data:
            BirdObservation.objects.create(observation=observation, **bird_data)

        return observation
