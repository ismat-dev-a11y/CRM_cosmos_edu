from django.db import models


class StoredFile(models.Model):
    class FileType(models.TextChoices):
        IMAGE    = "IMAGE", "Image"
        DOCUMENT = "DOCUMENT", "Document"
        VIDEO    = "VIDEO", "Video"

    file      = models.FileField(upload_to='files/')
    file_type = models.CharField(max_length=20, choices=FileType.choices, default=FileType.IMAGE)
    url       = models.URLField(blank=True)          # MinIO dan kelgan URL
    name      = models.CharField(max_length=255, blank=True)
    size      = models.PositiveIntegerField(default=0)  # bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # URL ni avtomatik hosil qilish
        if self.file and not self.url:
            self.url = self.file.url
        if self.file and not self.name:
            self.name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.file_type}"