from django.contrib import admin

from .models import Area, Region, Place


class ChangeOnlyAdmin(admin.ModelAdmin):
    """ Regions are editable (to add new areas) but deletion/addition handled programmatically """
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyAdmin(ChangeOnlyAdmin):
    """ Places are solely changed programmatically """
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Area)
admin.site.register(Region, ChangeOnlyAdmin)
admin.site.register(Place, ReadOnlyAdmin)
