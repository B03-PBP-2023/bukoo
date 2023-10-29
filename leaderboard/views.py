from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core import serializers 
from .models import Leaderboard
from book_collection.models import Book
from user_profile.models import Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

# Create your views here.
def get_popular_books(request, book_id):
    popular_books = get_object_or_404(Book, id=book_id)
    # popular = Leaderboard.objects.filter(book=popular_books)
    popular = Book.objects.annotate(leaderboard_count=Count('leaderboard')).order_by('-leaderboard_count')
    popular_books_data = []

    for rate in popular:
        author = [author.name for author in rate.author.all()]
        popular_books_data.append({
            'id': rate.id,
            'title': rate.title,
            'author': author,
        })
    return JsonResponse({'popular': popular_books_data})

# @login_required
def get_ratings_by_user(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    ratings = Leaderboard.objects.filter(userProfile=user_profile)
    ratings_data = []

    for rating in ratings:
        ratings_data.append({
            'id': rating.id,
            'title': rating.book.title,
            'rating': rating.is_recommended,
            'userProfile': rating.userProfile.user.username,
            'created_at': rating.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return JsonResponse({'user_ratings': ratings_data})

@login_required
def create_rating(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        user_profile = get_object_or_404(Profile, user=request.user)
        is_recommended = request.POST.get('is_recommended')

        if is_recommended in ['recommended', 'not_recommended']:
            # Membuat objek Leaderboard baru dengan is_recommended yang sesuai
            leaderboard = Leaderboard(book=book, userProfile=user_profile, is_recommended=is_recommended == 'recommended')
            leaderboard.save()
            return JsonResponse({'message': 'Rating added successfully'})
        else:
            return JsonResponse({'message': 'Invalid rating value'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required
def delete_rating(request, book_id):
    if request.method == 'POST':
        rating = get_object_or_404(Leaderboard, book__id=book_id)

        # Memeriksa apakah pengguna yang sedang login adalah pemilik penilaian
        if rating.userProfile.user == request.user:
            # Menghapus penilaian
            rating.delete()
            return JsonResponse({'message': 'Rating deleted successfully'})
        else:
            return JsonResponse({'message': 'You do not have permission to delete this rating'}, status=403)
        
@login_required
def edit_rating(request, rating_id):
    if request.method == 'POST':
        rating = get_object_or_404(Leaderboard, id=rating_id)

        # Memeriksa apakah pengguna yang sedang login adalah pemilik rating
        if rating.userProfile.user == request.user:
            new_is_recommended = request.POST.get('is_recommended')

            if new_is_recommended in ['recommended', 'not_recommend']:
                # Mengubah status rekomendasi berdasarkan nilai baru
                rating.is_recommended = new_is_recommended == 'recommend'
                rating.save()
                return JsonResponse({'message': 'Rating edited successfully'})
            else:
                return JsonResponse({'message': 'Invalid rating value'}, status=400)
        else:
            return JsonResponse({'message': 'You do not have permission to edit this rating'}, status=403)
        

def leaderboard_view(request):
    leaderboard_data = Leaderboard.objects.values('book__title').annotate(recommendation_count=Count('pk')).order_by('-recommendation_count')[:10]
    context = {'leaderboard_data': leaderboard_data}
    return render(request, 'leaderboard.html', context)