from django.shortcuts import redirect, render
from django.urls import reverse
from admin_dashboard.models import BookSubmission, AdminBook
from django.http import HttpResponseRedirect, JsonResponse
from admin_dashboard.form import BookDataForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import datetime
import json


def get_book_list(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        title = request.POST.get('title')
        language = request.POST.get('language')
        genre = request.POST.get('genre')
        isbn = request.POST.get('isbn')
        num_pages = request.POST.get('num_pages')
        description = request.POST.get('description')

        new_book = AdminBook(
            title=title,
            description=description,
            genres=genre,
            publisher=author,
            language=language,
            isbn=isbn,
            num_pages=num_pages
        )
        new_book.save()

        data_to_display = {
            'books': AdminBook.objects.all()
        }

        return render(request, 'admin.html', data_to_display)

    return render(request, 'admin.html', {'books': AdminBook.objects.all()})


def admin_dashboard(request):
    return render(request, 'admin.html')


def book_status(request):
    return render(request, '')


def create_book(request):
    form = BookDataForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('admin_dashboard:get_book_list'))

    context = {'form': form}
    return render(request, "admin2.html", context)


def admin2(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        title = request.POST.get('title')
        language = request.POST.get('language')
        genre = request.POST.get('genre')
        isbn = request.POST.get('isbn')
        num_pages = request.POST.get('num_pages')
        description = request.POST.get('description')

        # Simpan data ke database
        new_book = AdminBook(
            title=title,
            description=description,
            genres=genre,
            publisher=author,
            language=language,
            isbn=isbn,
            num_pages=num_pages
        )
        new_book.save()

        return HttpResponseRedirect(reverse('admin_dashboard:admin_dashboard'))

    return render(request, 'admin2.html')


def show_xml(request):
    data = BookSubmission.objects.all()
    xml_data = serializers.serialize(
        "xml", data, use_natural_foreign_keys=True)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    data = BookSubmission.objects.all()
    json_data = serializers.serialize(
        "json", data, use_natural_foreign_keys=True)
    return HttpResponse(json_data, content_type="application/json")


def show_xml_id(request, id):
    data = get_object_or_404(BookSubmission, pk=id)
    xml_data = serializers.serialize(
        "xml", [data], use_natural_foreign_keys=True)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json_id(request, id):
    data = get_object_or_404(BookSubmission, pk=id)
    json_data = serializers.serialize(
        "json", [data], use_natural_foreign_keys=True)
    return HttpResponse(json_data, content_type="application/json")


@csrf_exempt
def edit_book_submission(request, id):
    if request.method != 'POST':
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)
    if (not request.user.is_authenticated):
        return JsonResponse({'status': 'failed', 'message': 'Authentication required'}, status=401)
    if (not request.user.is_admin):
        return JsonResponse({'status': 'failed', 'message': 'Admin role is required'}, status=403)
    try:
        book_submission = BookSubmission.objects.get(pk=id)
    except BookSubmission.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'The book submission does not exist'}, status=404)
    
    data = json.loads(request.body)
    book_submission.status = data.get('status', book_submission.status)
    book_submission.feedback = data.get('feedback', book_submission.feedback)
    book_submission.timestamp = datetime.now()
    book_submission.save()
    return JsonResponse({'status': 'success', 'message': 'Book submission successfully updated'}, status=200)
