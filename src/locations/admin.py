from django.contrib import admin

from .models import Area, Region, Place

class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Area)
admin.site.register(Region)
admin.site.register(Place, ReadOnlyAdmin)
