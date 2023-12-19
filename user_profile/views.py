from django.shortcuts import render
from user_profile.models import Profile, Bookmark, Book_by_author
from user_profile.forms import ProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from book_collection.models import Book
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@login_required(login_url='/auth/login/')
def profile_data(request):
    bookmarked_book = Bookmark.objects.filter(user=request.user)
    user_data = Profile.objects.get(user=request.user)
    book_by_author = Book.objects.filter(author=user_data)

    if request.user.is_author == True:
        data = {
            'username': request.user.username,
            'name': user_data.name,
            'gender': user_data.gender,
            'birth_date': user_data.date_of_birth,
            'preferred_genre': user_data.prefered_genre,
            'description': user_data.about_user,
            'profile_picture': user_data.profile_picture,
            'written_books': book_by_author
        }
        return render(request, 'author_profile.html', data)
    else:
        data = {
            'username': request.user.username,
            'name': user_data.name,
            'gender': user_data.gender,
            'birth_date': user_data.date_of_birth,
            'preferred_genre': user_data.prefered_genre,
            'description': user_data.about_user,
            'profile_picture': user_data.profile_picture,
            'bookmarked_books': bookmarked_book,
        }

        return render(request, 'profile.html', data)


@csrf_exempt
@login_required(login_url='/auth/login/')
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile/')
    
    return render(request, 'edit_profile.html', {'form': form})


@csrf_exempt
@login_required(login_url='/auth/login/')
def get_bookmark_status(request, book_id):
    bookmark_exist = Bookmark.objects.filter(
        user=request.user, book=book_id).exists()
    return JsonResponse({'status': 'success', 'message': 'Bookmark status', 'data': bookmark_exist}, status=200)


@csrf_exempt
@login_required(login_url='/auth/login/')
@require_http_methods(['POST'])
def bookmarking_books(request, book_id):
    books = Book.objects.get(pk=book_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, book=books)

    if created:
        messages.success(request, 'Bookmarked')

        return HttpResponse("CREATED", status=201)

@csrf_exempt
@login_required(login_url='/auth/login/')
@require_http_methods(['POST'])
def delete_bookmark(request, book_id):
    bookmarks = Bookmark.objects.get(pk=book_id)
    bookmarks.delete()

    return HttpResponseRedirect('/profile/')





