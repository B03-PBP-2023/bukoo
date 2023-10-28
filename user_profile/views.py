from django.shortcuts import render
from user_profile.models import Profile, Bookmark
from user_profile.forms import ProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from book_collection.models import Book
from django.contrib.auth.decorators import login_required

@login_required
def profile_data(request):
    bookmarked_book = Bookmark.objects.filter(user=request.user)
    user_data = Profile.objects.filter(user=request.user)

    data = {
        'name': user_data.name,
        'gender': user_data.gender,
        'birth_date': user_data.date_of_birth,
        'prefered_genre': user_data.prefered_genre,
        'description': user_data.about_user,
        'bookmarked_books': bookmarked_book,
    }

    return render(request, 'profile.html', data)

@login_required
def edit_profile(request):
    profile = Profile.objects.get(pk=id)
    form = ProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile:user_profile'))
    
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def bookmarking_books(request, book_id):
    books = Book.objects.get(pk=book_id)
    Bookmark.objects.create(user=request.user, book=books)

    return HttpResponse("CREATED", status=201)

@login_required
def delet_bookmark(request, book_id):
    bookmarks = Bookmark.objects.get(pk=book_id)
    bookmarks.delete()

    return HttpResponseRedirect(reverse('profile:user_profile'))


