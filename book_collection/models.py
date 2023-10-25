from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from auth.models import User

# Create your models here.
class Genre(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self) -> str:
    return self.name

class MockAuthorProfile(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self) -> str:
    return self.name

class Book(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  image_url = models.URLField(null=True, blank=True)
  genres = models.ManyToManyField(Genre, blank=True)
  publisher = models.CharField(max_length=255, null=True, blank=True)
  author = models.ManyToManyField(MockAuthorProfile, blank=True)
  publish_date = models.DateField(null=True, blank=True)
  num_pages = models.IntegerField(validators=[MinLengthValidator(0)], null=True, blank=True)
  language = models.CharField(max_length=255, blank=True, null=True)
  isbn = models.CharField(max_length=13, validators=[MinLengthValidator(10)], null=True, blank=True)
  reviews_count = models.IntegerField(validators=[MinLengthValidator(0)], default=0)
  ratings_count = models.IntegerField(validators=[MinLengthValidator(0)], default=0)
  average_ratings = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(5)], decimal_places=1, max_digits=2, default=0)

  def __str__(self) -> str:
    return f"[{self.pk}] {self.title}"



