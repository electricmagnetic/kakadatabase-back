from django.contrib import admin

from .models import Bird

class BirdAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('__str__', 'area',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.all().select_related('area',)

admin.site.register(Bird, BirdAdmin)
