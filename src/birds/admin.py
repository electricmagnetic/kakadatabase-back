from django.contrib import admin

from .models import Bird


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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.all().select_related(
            'band_combo',
            'area',
        )


admin.site.register(Bird, BirdAdmin)
