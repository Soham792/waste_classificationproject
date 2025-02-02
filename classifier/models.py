from django.db import models

class ClassificationResult(models.Model):
    image = models.ImageField(upload_to='uploads/')
    predictions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Classification {self.id} - {self.created_at}"