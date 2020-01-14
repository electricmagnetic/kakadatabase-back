from django.contrib import admin

from .models import Bird, BirdProfile


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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.all().select_related(
            'bird_profile',
            'band_combo',
            'area',
        )


class BirdProfileAdmin(admin.ModelAdmin):
    list_filter = ('is_featured', )
    search_fields = ('bird__name', )


admin.site.register(Bird, BirdAdmin)
admin.site.register(BirdProfile, BirdProfileAdmin)
