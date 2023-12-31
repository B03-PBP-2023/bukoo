from django.db import models
from django.core.validators import MinLengthValidator


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"[{self.pk}] {self.name}"

    def natural_key(self):
        return {'id': self.pk, 'name': self.name}


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    author = models.ManyToManyField(to='user_profile.Profile', blank=True)
    publish_date = models.DateField(null=True, blank=True)
    num_pages = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.CharField(max_length=13, validators=[
                            MinLengthValidator(10)], null=True, blank=True)

    def __str__(self) -> str:
        return f"[{self.pk}] {self.title}"

    def natural_key(self):
        return {'id': self.pk, 'title': self.title, 'image_url': self.image_url, 'author': [author.name for author in self.author.all()], 'genres': [genre.name for genre in self.genres.all()], 'publisher': self.publisher, 'publish_date': self.publish_date, 'num_pages': self.num_pages, 'language': self.language, 'isbn': self.isbn, 'description': self.description}
