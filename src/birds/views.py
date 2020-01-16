from django_filters import rest_framework as filters
from rest_framework import viewsets, response
#from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404

from .models import Bird
from .serializers import BirdSerializer


class BirdFilter(filters.FilterSet):
    """ Adding custom filters to check whether Bird is featured, extended (with profile), or has a band assigned (plus normal filters)"""
    is_extended = filters.BooleanFilter(
        field_name='profile__is_extended',
        lookup_expr='isnull',
        exclude=True,
        label='Is extended'
    )
    is_featured = filters.BooleanFilter(
        field_name='profile__is_featured', label='Is featured'
    )
    has_band = filters.BooleanFilter(
        field_name='band_combo',
        lookup_expr='isnull',
        exclude=True,
        label='Has band'
    )

    class Meta:
        model = Bird
        fields = (
            'sex',
            'status',
            'area',
        )


class SlugOrIdLookupMixin(object):
    """
    Apply this mixin to any view or viewset to filter by slug and id, instead of the
    default single field filtering.
    """
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        try:
            # Attempt with pk first
            obj = get_object_or_404(queryset, **filter_kwargs)
        except:
            # If unsuccessful, try with the pk as a slug instead
            filter_kwargs['slug'] = filter_kwargs.pop('pk')
            obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class BirdViewSet(SlugOrIdLookupMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Bird.objects. \
               select_related('area', 'band_combo', 'profile',). \
               all()
    serializer_class = BirdSerializer
    search_fields = ('name', 'band_combo__combo')
    ordering_fields = (
        'name',
        'status',
        'area',
        'profile',
    )
    filter_class = BirdFilter
