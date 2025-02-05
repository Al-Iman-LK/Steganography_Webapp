from django.contrib import admin
from .models import SteganoFile

@admin.register(SteganoFile)
class SteganoFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_type', 'status', 'created_at', 'auto_delete')
    list_filter = ('file_type', 'status', 'auto_delete')
    search_fields = ('user__username', 'original_file')
    readonly_fields = ('created_at', 'updated_at')
