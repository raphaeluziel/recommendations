from django.contrib import admin
from django.forms import TextInput, Textarea

from .models import Responses

# Register your models here.

class ResponsesAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    ordering = ('student__last_name',)
    list_per_page = 50

admin.site.register(Responses, ResponsesAdmin)
