from django.db import models



class Document(models.Model):
    TYPE_CHOICES = (
        ("local", "Local File"),
        ("remote", "Remote URL"),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    file = models.FileField(upload_to="documents/", blank=True, null=True)
    file_url = models.URLField(max_length=1024, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name