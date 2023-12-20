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
from admin_dashboard.models import BookSubmission
from review.models import Review
from forum.models import ForumDiscuss
from forum.models import Reply


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
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Profile not found'}, status=404)
    statistics = {
        'total_bookmarked': Bookmark.objects.filter(user=request.user).count(),
        'total_review': Review.objects.filter(userProfile=profile).count(),
        'total_forum_discussion': ForumDiscuss.objects.filter(user=profile).count(),
        'total_replies': Reply.objects.filter(user=profile).count(),
    }
    if request.user.is_author:
        statistics['total_book_submitted'] = Book.objects.filter(author=profile).count()

    data = {
        'id': profile.pk,
        'name': profile.name,
        'about_user': profile.about_user,
        'date_of_birth': profile.date_of_birth,
        'gender': profile.gender,
        'prefered_genre': profile.prefered_genre,
        'profile_picture': profile.profile_picture,
        'statistics': statistics
    }
    return JsonResponse({'status': 'success', 'message': 'Profile data', 'data': data}, status=200)


def show_xml_id(request, id):
    data = get_object_or_404(Profile, pk=id)
    return HttpResponse(serializers.serialize("xml", [data], use_natural_foreign_keys=True), content_type="application/xml")


def show_json_id(request, id):
    data = get_object_or_404(Profile, pk=id)
    return HttpResponse(serializers.serialize("json", [data], use_natural_foreign_keys=True), content_type="application/json")


@csrf_exempt
def get_bookmarks_by_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'failed', 'message': 'Authentication required'}, status=401)

    bookmarks = Bookmark.objects.filter(user=request.user)
    bookmarked_books = []
    for bookmark in bookmarks:
        bookmarked_books.append({
            'id': bookmark.pk,
            'book': {
                'id': bookmark.book.pk,
                'title': bookmark.book.title,
                'image_url': bookmark.book.image_url,
                'author': bookmark.book.author.name,
            }})
    return JsonResponse({'status': 'success', 'data': bookmarked_books}, status=200)


@csrf_exempt
def get_booksubmission_by_author(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'failed', 'message': 'Authentication required'}, status=401)
    user_profile = Profile.objects.get(user=request.user)
    book_submissions = BookSubmission.objects.filter(
        book__author__id=user_profile.id)
    data = serializers.serialize(
        'json', book_submissions, use_natural_foreign_keys=True)
    return HttpResponse(data, content_type="application/json")
