from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Review
from book_collection.models import Book
from user_profile.models import Profile

def get_reviews_by_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)
    review_data = []
    for review in reviews:
        review_data.append({
            'id': review.id,
            'review': review.review,
            'userProfile': review.userProfile.user.username,
            'created_at': review.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return JsonResponse({'reviews': review_data})

def create_review(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        user_profile = get_object_or_404(Profile, user=request.user)
        review_text = request.POST.get('review', '')
        if review_text:
            review = Review(book=book, review=review_text, userProfile=user_profile)
            review.save()
            return JsonResponse({'message': 'Review added successfully'})
        else:
            return JsonResponse({'message': 'Review text cannot be empty'}, status=400)

def delete_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        if review.userProfile.user == request.user:
            review.delete()
            return JsonResponse({'message': 'Review deleted successfully'})
        else:
            return JsonResponse({'message': 'You do not have permission to delete this review'}, status=403)

def edit_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        if review.userProfile.user == request.user:
            new_review_text = request.POST.get('review', '')
            if new_review_text:
                review.review = new_review_text
                review.save()
                return JsonResponse({'message': 'Review edited successfully'})
            else:
                return JsonResponse({'message': 'Review text cannot be empty'}, status=400)
        else:
            return JsonResponse({'message': 'You do not have permission to edit this review'}, status=403)


# Create your views here.
