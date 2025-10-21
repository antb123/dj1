from django.contrib import admin
from .models import Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    """Admin configuration for Folder model."""

    list_display = ('name', 'owner', 'parent', 'created_at', 'get_file_count')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')

    def get_file_count(self, obj):
        return obj.get_file_count()
    get_file_count.short_description = 'Files'
