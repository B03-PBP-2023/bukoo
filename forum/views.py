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
from django.core import serializers


# update
@csrf_exempt
def create_forum_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        new_data = ForumDiscuss.objects.create(
            user=request.user,
            subject=data["subject"],
            description=data["description"],
        )

        new_data.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

# update


@csrf_exempt
def create_reply_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        forum = ForumDiscuss.objects.get(pk=data["forum_id"])

        reply = Reply.objects.create(
            user=request.user,
            message=data["message"],
            forum=forum
        )

        reply.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)


# update
def show_json_by_userForum(request):
    data = ForumDiscuss.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# update
def show_json_by_userReply(request):
    data = Reply.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


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
        # Menggunakan get untuk menghindari KeyError
        'last_login': request.COOKIES.get('last_login', ''),
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

    forums = ForumDiscuss.objects.filter(book=book)
    forum_json = []
    for forum in forums:
        forum_json.append({
            "user": {
                "id": forum.user.pk,
                "name": forum.user.name,
                "profile_picture": forum.user.profile_picture.url if forum.user.profile_picture else "",
            },
            "subject": forum.subject,
            "description": forum.description,
            "date_added": forum.date_added,
            "id": forum.pk,
            "total_reply": forum.total_reply,
        })
    
    book_json = {
        "id": book.pk,
        "title": book.title,
        "image_url": book.image_url,
        "author": [author.name for author in book.author.all()],
    }

    return JsonResponse({'book': book_json, 'forums':forum_json}, safe=False)


def get_reply_json(request, id):
    try:
        forum = ForumDiscuss.objects.get(pk=id)
    except (Book.DoesNotExist, ForumDiscuss.DoesNotExist):
        return JsonResponse({'error': 'Book or Forum not found'}, status=404)

    replies = Reply.objects.filter(forum=forum)
    replies_json = []
    for reply in replies:
        replies_json.append({
            "user": {
                "id": reply.user.pk,
                "name": reply.user.name,
                "profile_picture": reply.user.profile_picture.url if reply.user.profile_picture else "",
            },
            "created_at": reply.created_at,
            "message": reply.message,
            "id": reply.pk,
        })

    return JsonResponse(replies_json, safe=False)


@csrf_exempt
def add_forum_ajax(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=403)
    if request.method == 'POST':
        json_data = json.loads(request.body)
        subject = json_data.get("subject", "").strip()
        description = json_data.get("description", "").strip()
        user = get_object_or_404(Profile, user=request.user)
        book_id = id

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Book not found'}, status=404)

        if subject and description:
            new_forum = ForumDiscuss(
                subject=subject, description=description, user=user, book=book)
            new_forum.save()
            return JsonResponse({'status': 'success', 'message': 'Forum has been created.'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': 'Subject and description are required'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


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
