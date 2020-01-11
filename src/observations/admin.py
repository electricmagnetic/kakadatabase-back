from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Contributor, Observation, BirdObservation


class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'email',
        'activity',
        'heard',
    )


class BirdObservationInline(admin.TabularInline):
    model = BirdObservation
    extra = 0
    raw_id_fields = ('bird', )


def mark_public(modeladmin, request, queryset):
    queryset.update(status='public')
    mark_public.short_description = "Mark selected as Public"


class ObservationAdmin(LeafletGeoAdmin):
    list_display = (
        'id',
        '__str__',
        'contributor',
        'geocode',
        'region',
        'favourite',
        'confirmed',
        'status',
        'date_created',
    )
    list_filter = (
        'status',
        'date_created',
        'favourite',
        'region',
        'confirmed',
    )
    inlines = [BirdObservationInline]
    readonly_fields = (
        'geocode',
        'region',
    )
    actions = [mark_public]


class BirdObservationAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'banded',
        'sex_guess',
        'life_stage_guess',
        'band_combo',
        'bird',
        'revisit',
    )
    list_filter = ('revisit', )
    raw_id_fields = ('bird', )


admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Observation, ObservationAdmin)
admin.site.register(BirdObservation, BirdObservationAdmin)
