from django.db import models
from django.conf import settings


class Folder(models.Model):
    """Model representing a folder for organizing documents."""

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='folders')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['owner', 'parent', 'name']

    def __str__(self):
        return self.get_full_path()

    def get_full_path(self):
        """Get the full path of the folder including parent folders."""
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name

    def get_children(self):
        """Get all child folders."""
        return self.children.all()

    def get_file_count(self):
        """Get the total number of files in this folder."""
        return self.documents.count()

    def get_total_size(self):
        """Get the total size of all files in this folder."""
        total = self.documents.aggregate(total=models.Sum('file_size'))['total']
        return total or 0

    def get_all_descendants(self):
        """Get all descendant folders recursively."""
        descendants = list(self.children.all())
        for child in list(descendants):
            descendants.extend(child.get_all_descendants())
        return descendants

    def is_ancestor_of(self, folder):
        """Check if this folder is an ancestor of the given folder."""
        if folder.parent is None:
            return False
        if folder.parent == self:
            return True
        return self.is_ancestor_of(folder.parent)
