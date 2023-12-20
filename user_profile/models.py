from django.db import models
from auth.models import User
from book_collection.models import Book


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    about_user = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    prefered_genre = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return f"[{self.pk}] {self.name}"

    def natural_key(self):
        name = self.name
        about_user = self.about_user
        date_of_birth = self.date_of_birth
        gender = self.gender
        preferred_genre = self.prefered_genre
        profile_picture = self.profile_picture
        
        if self.user:
            self.user.username
        return {'id':self.pk, 'name':name, 'about_user': about_user, 'date_of_birth': date_of_birth, 'gender': gender, 'prefered_genre': preferred_genre, 'profile_picture': profile_picture}

class Bookmark(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Book_by_author(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
