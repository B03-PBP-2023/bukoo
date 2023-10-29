from django.db import models

class AdminBook(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    genres = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    num_pages = models.PositiveIntegerField(null=True, blank=True)
    publish_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"[{self.pk}] {self.title}"
