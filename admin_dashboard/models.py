from django.db import models

class BookSubmission(models.Model):
    # STATUS_CHOICES = (
    #     ('pending', 'Pending'),
    #     ('verified', 'Verified'),
    # )
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.title
# Create your models here.
