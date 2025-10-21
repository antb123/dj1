from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import hashlib
import os


def user_directory_path(instance, filename):
    """Generate upload path for document files."""
    # Get file extension
    ext = os.path.splitext(filename)[1]
    # Generate unique filename
    hash_obj = hashlib.md5(f"{instance.owner.id}{filename}".encode())
    unique_filename = f"{hash_obj.hexdigest()}{ext}"

    # Return path: documents/<user_id>/<folder_id>/<filename>
    folder_id = instance.folder.id if instance.folder else 'root'
    return f'documents/{instance.owner.id}/{folder_id}/{unique_filename}'


class Document(models.Model):
    """Model representing an uploaded document."""

    FILE_TYPE_CHOICES = [
        ('txt', 'Text'),
        ('md', 'Markdown'),
        ('pdf', 'PDF'),
        ('doc', 'Word Document'),
        ('docx', 'Word Document (DOCX)'),
    ]

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    file_size = models.BigIntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    folder = models.ForeignKey('folders.Folder', on_delete=models.CASCADE, null=True, blank=True, related_name='documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checksum = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['owner', 'folder']),
            models.Index(fields=['file_type']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save to calculate file size and checksum."""
        if self.file:
            # Set file size
            self.file_size = self.file.size

            # Validate file type
            ext = self.get_file_extension()
            if ext not in settings.ALLOWED_FILE_TYPES:
                raise ValidationError(f"File type {ext} is not allowed.")

            # Set file type based on extension
            ext_to_type = {
                '.txt': 'txt',
                '.md': 'md',
                '.pdf': 'pdf',
                '.doc': 'doc',
                '.docx': 'docx',
            }
            self.file_type = ext_to_type.get(ext, 'txt')

            # Calculate checksum
            if not self.checksum:
                self.file.seek(0)
                file_hash = hashlib.sha256()
                for chunk in self.file.chunks():
                    file_hash.update(chunk)
                self.checksum = file_hash.hexdigest()
                self.file.seek(0)

        super().save(*args, **kwargs)

        # Update user's storage usage
        if self.owner:
            self.owner.update_storage_used()

    def delete(self, *args, **kwargs):
        """Override delete to update user storage and remove file."""
        # Delete the file from storage
        if self.file:
            self.file.delete(save=False)

        super().delete(*args, **kwargs)

        # Update user's storage usage
        if self.owner:
            self.owner.update_storage_used()

    def get_file_extension(self):
        """Get the file extension."""
        return os.path.splitext(self.file.name)[1].lower()

    def get_readable_size(self):
        """Return human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"

    def get_icon_class(self):
        """Return icon class based on file type."""
        icons = {
            'txt': 'file-text',
            'md': 'file-code',
            'pdf': 'file-pdf',
            'doc': 'file-word',
            'docx': 'file-word',
        }
        return icons.get(self.file_type, 'file')
