from django.db import models

# Create your models here.
from book_collection.models import Book  
from user_profile.models import Profile

class Leaderboard(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    userProfile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation by {self.userProfile.user.username} for {self.book.title}"

    