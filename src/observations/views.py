import django_filters
from rest_framework import viewsets

from .models import Observation, BirdObservation
from .serializers import ObservationSerializer, BirdObservationSerializer


class ObservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Observation.objects. \
               select_related('contributor',). \
               exclude(status='private').\
               exclude(status='invalid')
    serializer_class = ObservationSerializer
    filter_fields = (
        'observation_type',
        'status',
        'confirmed',
    )
    ordering_fields = (
        'contributor',
        'region',
        'date_sighted',
        'time_sighted',
        'date_created',
        'date_updated',
    )


class BirdObservationFilter(django_filters.FilterSet):
    has_bird = django_filters.BooleanFilter(
        field_name='bird', lookup_expr='isnull', exclude=True, label='Has bird'
    )

    class Meta:
        model = BirdObservation
        fields = (
            'observation',
            'bird',
        )


class BirdObservationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BirdObservationSerializer
    ordering = (
        '-observation__date_sighted',
        '-observation__time_sighted',
    )
    ordering_fields = (
        'id',
        'banded',
        'observation',
        'observation__date_sighted',
        'observation__time_sighted',
        'bird',
    )
    filter_class = BirdObservationFilter

    def get_queryset(self):
        queryset = BirdObservation.objects. \
        exclude(observation__status='private'). \
        exclude(observation__status='bad')

        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
