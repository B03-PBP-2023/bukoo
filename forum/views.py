from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import ForumDiscuss, Book, Reply
from user_profile.models import Profile
from .forms import ForumForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

def show_forum(request, id):
    # Menggunakan get_object_or_404 untuk mendapatkan objek Book atau memberikan 404 jika tidak ditemukan
    book = get_object_or_404(Book, pk=id)
    # Menggunakan filter untuk mendapatkan semua forum terkait dengan buku ini
    forums = ForumDiscuss.objects.filter(book=book)
    # # Jika form dikirimkan, proses form
    # if request.method == 'POST':
    #     form = ForumForm(request.POST)
    #     if form.is_valid():
    #         new_forum = form.save(commit=False)

    #         new_forum.book = book
    #         new_forum.save()
    # else:
    form = ForumForm()
    context = {
        'forums': forums,
        'book':  book,
        'last_login': request.COOKIES.get('last_login', ''),  # Menggunakan get untuk menghindari KeyError
        # 'username': request.user.username,
        # 'pk': request.user.pk,
        'form': form,
    }
    return render(request, "forum.html", context)

def get_forum_json(request, id):
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    forum_items = ForumDiscuss.objects.filter(book=book).values(
        "user", "user__name", "date_added", "subject", "description", "pk"
    )

    return JsonResponse(list(forum_items), safe=False)

def get_reply_json(request, id):
    try:
        forum = ForumDiscuss.objects.get(pk=id)
    except (Book.DoesNotExist, ForumDiscuss.DoesNotExist):
        return JsonResponse({'error': 'Book or Forum not found'}, status=404)

    reply_items = Reply.objects.filter(forum=forum).values(
        "user", "user__username", "message", "pk"
    )

    return JsonResponse(list(reply_items), safe=False)

@csrf_exempt
def add_forum_ajax(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=403)
    if request.method == 'POST':
        subject = request.POST.get("subject", "").strip()
        description = request.POST.get("description", "").strip()
        user = get_object_or_404(Profile, user=request.user)
        book_id = id

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)

        if subject and description:
            new_forum = ForumDiscuss(subject=subject, description=description, user=user, book=book)
            new_forum.save()
            return JsonResponse({'status': 'CREATED'}, status=201)
        else:
            return JsonResponse({'error': 'Subject and description are required'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def add_reply_ajax(request, forum_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=403)
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            message = data.get("message", "").strip()
            user = get_object_or_404(Profile, user=request.user)
            forum = ForumDiscuss.objects.get(pk=forum_id)

            forum.total_reply += 1
            forum.save()

            if message:
                new_reply = Reply(message=message, user=user, forum=forum)
                new_reply.save()
                return JsonResponse({'status': 'CREATED'}, status=201)
            else:
                return JsonResponse({'error': 'Message is required'}, status=400)

        except (Book.DoesNotExist, ForumDiscuss.DoesNotExist):
            return JsonResponse({'error': 'Book or Forum not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


