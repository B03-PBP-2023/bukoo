from django.db import models

# Create your models here.
from book_collection.models import Book  
from user_profile.models import Profile

class Leaderboard(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    userProfile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    is_recommendation = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation by {self.userProfile.user.username} for {self.book.title}"

    