from django.contrib import admin
from django.forms import TextInput, Textarea

from .models import Responses

# Register your models here.

class ResponsesAdmin(admin.ModelAdmin):

    """
        This is respobsible for the display Responses section of the
        Django Admin site
    """

    list_display = ('status', 'get_first_name', 'get_last_name',)
    list_display_links = ('status',)
    list_filter = ('status',)
    ordering = ('student__last_name',)
    list_per_page = 50

    # This will get the field first_name and then the last_name from student
    # for ordering in the admin page
    def get_first_name(self, obj):
        return obj.student.first_name
    get_first_name.short_description = "first_name"
    get_first_name.admin_order_field = "student__first_name"

    def get_last_name(self, obj):
        return obj.student.last_name
    get_last_name.short_description = "last_name"
    get_last_name.admin_order_field = "student__last_name"

admin.site.register(Responses, ResponsesAdmin)
