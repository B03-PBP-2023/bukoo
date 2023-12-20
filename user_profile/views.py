from django.shortcuts import render
from user_profile.models import Profile, Bookmark, Book_by_author
from user_profile.forms import ProfileForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from book_collection.models import Book
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core import serializers


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
            return JsonResponse({'status': 'success', 'message': 'Profile updated'}, status=200)
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid form'}, status=400)

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
    try:
        books = Book.objects.get(pk=book_id)
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user, book=books)
        messages.success(request, 'Bookmarked')
        return JsonResponse({'status': 'success', 'message': 'Bookmarked'}, status=201)
    except Book.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Book not found'}, status=404)


@csrf_exempt
@login_required(login_url='/auth/login/')
@require_http_methods(['POST'])
def delete_bookmark(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
        bookmarks = Bookmark.objects.get(user=request.user, book=book)
        bookmarks.delete()
        return JsonResponse({'status': 'success', 'message': 'Bookmark deleted'}, status=200)
    except Book.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Book not found'}, status=404)
    except Bookmark.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Bookmark not found'}, status=404)


def show_xml(request):
    data = Profile.objects.all()
    return HttpResponse(serializers.serialize("xml", data, use_natural_foreign_keys=True), content_type="application/xml")


def show_json(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'failed', 'message': 'Authentication required'}, status=401)
    try:
        data = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Profile not found'}, status=404)
    
    data = {
        'id': data.pk,
        'name': data.name,
        'about_user': data.about_user,
        'date_of_birth': data.date_of_birth,
        'gender': data.gender,
        'prefered_genre': data.prefered_genre,
        'profile_picture': data.profile_picture,
    }
    return JsonResponse({'status': 'success', 'message': 'Profile data', 'data': data}, status=200)


def show_xml_id(request, id):
    data = get_object_or_404(Profile, pk=id)
    return HttpResponse(serializers.serialize("xml", [data], use_natural_foreign_keys=True), content_type="application/xml")


def show_json_id(request, id):
    data = get_object_or_404(Profile, pk=id)
    return HttpResponse(serializers.serialize("json", [data], use_natural_foreign_keys=True), content_type="application/json")
