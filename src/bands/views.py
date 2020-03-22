from rest_framework import viewsets

from .models import BandCombo
from .serializers import BandComboSerializer


class BandComboViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BandComboSerializer
    pagination_class = None
    search_fields = ('combo', 'bird__name', 'bird__primary_band')
    ordering_fields = (
        'combo',
        'bird__name',
    )

    def get_queryset(self):
        queryset = BandCombo.objects. \
                   select_related('bird'). \
                   all()

        return queryset
