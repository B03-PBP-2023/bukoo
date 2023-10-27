from django.db import models
from django.core.validators import MinLengthValidator
from auth.models import User

class Genre(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self) -> str:
    return f"[{self.pk}] {self.name}"

  def natural_key(self):
    return {'id':self.pk, 'name':self.name}


# TODO: integrate with user_profile module
class MockAuthorProfile(models.Model):
  name = models.CharField(max_length=255)
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

  def __str__(self) -> str:
    return f"[{self.pk}] {self.name}"
  
  def natural_key(self):
    return {'id':self.pk, 'name':self.name}


class Book(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  image_url = models.URLField(null=True, blank=True)
  genres = models.ManyToManyField(Genre, blank=True)
  publisher = models.CharField(max_length=255, null=True, blank=True)
  author = models.ManyToManyField(MockAuthorProfile, blank=True)
  publish_date = models.DateField(null=True, blank=True)
  num_pages = models.PositiveIntegerField(null=True, blank=True)
  language = models.CharField(max_length=255, blank=True, null=True)
  isbn = models.CharField(max_length=13, validators=[MinLengthValidator(10)], null=True, blank=True)

  def __str__(self) -> str:
    return f"[{self.pk}] {self.title}"

  def natural_key(self):
    return (self.pk, self.title)


