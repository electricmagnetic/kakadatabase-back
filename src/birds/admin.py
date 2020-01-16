from django.contrib import admin

from .models import Bird, BirdProfile
from bands.models import BandCombo


class BandComboInline(admin.StackedInline):
    model = BandCombo


class BirdAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
        'primary_band',
    )
    list_display = (
        '__str__',
        'sex',
        'status',
        'primary_band',
        'band_combo',
        'area',
    )
    readonly_fields = ('id', )
    inlines = [BandComboInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.all().select_related(
            'profile',
            'band_combo',
            'area',
        )


class BirdProfileAdmin(admin.ModelAdmin):
    list_filter = ('is_featured', )
    search_fields = ('bird__name', 'bird__primary_band')


admin.site.register(Bird, BirdAdmin)
admin.site.register(BirdProfile, BirdProfileAdmin)
