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
import datetime


@csrf_exempt
def delete_forum_flutter(request, forum_id):
    if request.method == 'POST':
        # Deleting an existing forum
        forum = get_object_or_404(ForumDiscuss, id=forum_id)
        forum.delete()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error", 'message': 'Invalid request method'}, status=401)

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
    user_profile = Profile.objects.get(user=request.user)
    forums = ForumDiscuss.objects.filter(user=user_profile)
    data = []
    for forum in forums:
        data.append({
            "id": forum.pk,
            "subject": forum.subject,
            "description": forum.description,
            "date_added": forum.date_added,
            "total_reply": forum.total_reply,
            "book": {
                "id": forum.book.pk,
                "title": forum.book.title,
                "image_url": forum.book.image_url,
                "author": list(author.name for author in forum.book.author.all()),
            },
        })
    return JsonResponse({"status": "success", "data": data}, status=200)


# update
def show_json_by_userReply(request):
    user_profile = Profile.objects.get(user=request.user)
    replies = Reply.objects.filter(user=user_profile)
    data = []
    for reply in replies:
        data.append({
            "created_at": reply.created_at,
            "message": reply.message,
            "id": reply.pk,
            "forum": {
                "id": reply.forum.pk,
                "subject": reply.forum.subject,
                "description": reply.forum.description,
                "date_added": reply.forum.date_added,
            },
            "book": {
                "id": reply.forum.book.pk,
                "title": reply.forum.book.title,
                "image_url": reply.forum.book.image_url,
                "author": list(author.name for author in reply.forum.book.author.all()),
            },
        })
    return JsonResponse({"status": "success", "data": data}, status=200)


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

    return JsonResponse({'book': book_json, 'forums': forum_json}, safe=False)


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
                return JsonResponse({'status': 'success', 'message': f'Reply to forum ${forum_id} has been created.'}, status=201)
            else:
                return JsonResponse({'status': 'error', 'message': 'Message are required'}, status=400)

        except (Book.DoesNotExist, ForumDiscuss.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Book or Forum are not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def edit_reply(request, reply_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=403)
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            message = data.get("message", "").strip()
            if message:
                reply = Reply.objects.get(pk=reply_id)
                reply.message = message
                reply.created_at = datetime.datetime.now()
                reply.save()
                return JsonResponse({'status': 'success', 'message': f'Reply with id {reply_id} has been modified.'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Message are required'}, status=400)

        except (Reply.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Reply is not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def delete_reply(request, reply_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=403)
    if request.method == 'POST':
        try:
            reply = Reply.objects.get(pk=reply_id)
            reply.delete()
            return JsonResponse({'status': 'success', 'message': f'Reply with id {reply_id} has been deleted.'}, status=200)
        except (Reply.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Reply is not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
