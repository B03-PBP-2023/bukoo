from django.db import models
from book_collection.models import Book

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

class BookSubmission(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='pending') # pending, verified, rejected
    feedback = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)