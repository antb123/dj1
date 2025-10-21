from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin configuration for Document model."""

    list_display = ('name', 'owner', 'folder', 'file_type', 'get_size', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at', 'owner')
    search_fields = ('name', 'owner__email')
    readonly_fields = ('file_size', 'checksum', 'uploaded_at', 'updated_at')

    def get_size(self, obj):
        return obj.get_readable_size()
    get_size.short_description = 'Size'
