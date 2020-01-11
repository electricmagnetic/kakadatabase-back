from rest_framework import viewsets

from .models import Bird
from .serializers import BirdSerializer


class BirdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bird.objects. \
               select_related('area', 'band_combo',). \
               all()
    serializer_class = BirdSerializer
    search_fields = ('name', )
    ordering_fields = ('name', )
