from django.db import models
from book_collection.models import Book  
from user_profile.models import Profile  

class Review(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    review = models.TextField()
    userProfile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.userProfile.user.username} for {self.book.title}"

# Create your models here.
