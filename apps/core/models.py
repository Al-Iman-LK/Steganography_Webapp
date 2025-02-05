from django.db import models
from django.contrib.auth import get_user_model

class SteganoFile(models.Model):
    PROCESSING_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    FILE_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    original_file = models.FileField(upload_to='uploads/')
    processed_file = models.FileField(upload_to='processed/', null=True, blank=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    hidden_message = models.TextField(blank=True)
    extracted_message = models.TextField(blank=True)
    extraction_date = models.DateTimeField(null=True, blank=True)
    extraction_status = models.CharField(
        max_length=10, 
        choices=PROCESSING_STATUS,
        default='pending'
    )
    status = models.CharField(max_length=10, choices=PROCESSING_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auto_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.file_type} - {self.user.username} - {self.status}"
