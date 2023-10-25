from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Leaderboard
from book_collection.models import Book
from user_profile.models import Profile
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Create your views here.
def get_popular_books(request, book_id):
    popular_books = get_object_or_404(Book, id=book_id)
    popular = Leaderboard.objects.filter(book=popular_books)
    popular_books_data = []

    for rate in popular:
        popular_books_data.append({
            'id': rate.id,
            'title': rate.title,
            'rating': rate.rating,
            'userProfile': rate.userProfile.user.username,
            'created_at': rate.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return JsonResponse({'popular': popular_books_data})

def get_best_books(request, book_id):
    best_books = get_object_or_404(Book, id=book_id)
    best_book = Leaderboard.objects.filter(book=best_books)
    best_books_data = []

    for best in best_book:
        best_books_data.append({
            'id': best.id,
            'title': best.title,
            'best': best.best,
            'userProfile': best.userProfile.user.username,
            'created_at': best.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return JsonResponse({'best_book': best_books_data})

def get_ratings_by_user(request, user_id):
    user_profile = get_object_or_404(Profile, user_id=user_id)
    ratings = Profile.objects.filter(userProfile=user_profile)
    ratings_data = []

    for rating in ratings:
        ratings_data.append({
            'id': rating.id,
            'title': rating.title,
            'rating': rating.rating,
            'userProfile': rating.userProfile.user.username,
            'created_at': rating.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return JsonResponse({'user_ratings': ratings_data})


def create_rating(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        user_profile = get_object_or_404(Profile, user=request.user)
        is_recommendation = request.POST.get('is_recommendation')

        if is_recommendation in ['recommend', 'not_recommend']:
            # Membuat objek rating baru
            rating = Leaderboard(book=book, userProfile=user_profile, is_recommendation=is_recommendation == 'recommend')
            rating.save()
            return JsonResponse({'message': 'Rating added successfully'})
        else:
            return JsonResponse({'message': 'Invalid rating value'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)


def delete_rating(request, rating_id):
    if request.method == 'POST':
        rating = get_object_or_404(Book, id=rating_id)

        # Memeriksa apakah pengguna yang sedang login adalah pemilik penilaian
        if rating.userProfile.user == request.user:
            # Menghapus penilaian
            rating.delete()
            return JsonResponse({'message': 'Rating deleted successfully'})
        else:
            return JsonResponse({'message': 'You do not have permission to delete this rating'}, status=403)
        

def edit_rating(request, rating_id):
    if request.method == 'POST':
        rating = get_object_or_404(Leaderboard, id=rating_id)

        # Memeriksa apakah pengguna yang sedang login adalah pemilik rating
        if rating.userProfile.user == request.user:
            new_is_recommendation = request.POST.get('is_recommendation')

            if new_is_recommendation in ['recommend', 'not_recommend']:
                # Mengubah status rekomendasi berdasarkan nilai baru
                rating.is_recommendation = new_is_recommendation == 'recommend'
                rating.save()
                return JsonResponse({'message': 'Rating edited successfully'})
            else:
                return JsonResponse({'message': 'Invalid rating value'}, status=400)
        else:
            return JsonResponse({'message': 'You do not have permission to edit this rating'}, status=403)
        
def get_user_recommendation_count(user_profile):
    return Leaderboard.objects.filter(userProfile=user_profile, is_recommendation=True).count()
