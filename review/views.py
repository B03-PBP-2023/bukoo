from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.core import serializers
from django.http import JsonResponse
from .models import Review
from .forms import ReviewForm
from book_collection.models import Book
from user_profile.models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def get_reviews_by_book(request, book_id):
    book = get_object_or_404(Book, id= book_id)
    user_has_reviewed = has_reviewed(request, book_id)
    print(user_has_reviewed)
    return render(request, "review_book.html", {'book': book, 'has_reviewed': user_has_reviewed})

def get_review_json(request, book_id):
    print("masuk json")
    
    book = get_object_or_404(Book, pk=book_id)
    review_item = Review.objects.filter(book=book).order_by('-created_at')
    return HttpResponse(serializers.serialize('json', review_item, use_natural_foreign_keys=True))

def get_book_json(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return HttpResponse(serializers.serialize('json', [book]))


@login_required
def create_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    type(book)
   
    if request.method == 'POST':
        print("masuk post")
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            profile, created = Profile.objects.get_or_create(user=request.user)
            review.userProfile = profile
            review.save()
            print("masuk valid gasi")
            return JsonResponse({'message': 'Review added successfully'})

    form = ReviewForm()
    return render(request, 'create_review.html', {'form': form, 'book': book})

@login_required
def delete_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        if review.userProfile.user == request.user:
            review.delete()
            return JsonResponse({'message': 'Review deleted successfully'})
        else:
            return JsonResponse({'message': 'You do not have permission to delete this review'}, status=403)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
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
    form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form, 'review' : review})

def has_reviewed(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    profile = get_object_or_404(Profile, user=request.user)
    review = Review.objects.filter(book=book, userProfile=profile)
    if review:
        return True
    else:
        return False
# Create your views here.
