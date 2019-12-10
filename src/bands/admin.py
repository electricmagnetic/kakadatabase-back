from django.contrib import admin

from .models import BandCombo

class BandComboAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'bird', 'date_modified',)
    search_fields = ('combo__icontains', 'bird__name',)
    readonly_fields = ('colours', 'leg_left', 'leg_right',)

admin.site.register(BandCombo, BandComboAdmin)
