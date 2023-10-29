from django.shortcuts import render
from user_profile.models import Profile, Bookmark
from user_profile.forms import ProfileForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from book_collection import Book

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

def edit_profile(request):
    profile = Profile.objects.get(pk=id)
    form = ProfileForm(request.POST or None, instance=profile)

    if form.is_valid() and request.method == 'POST':
        form.save()
        return HttpResponseRedirect(reverse('user_profile:profile'))
    
    return render(request, 'edit_profile.html', {'form': form})

def bookmarking_books(request, book_id):
    books = Book


