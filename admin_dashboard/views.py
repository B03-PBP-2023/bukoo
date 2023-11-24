from django.shortcuts import redirect, render
from django.urls import reverse
from admin_dashboard.models import AdminBook
from django.http import HttpResponseRedirect, JsonResponse
from admin_dashboard.form import BookDataForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import get_object_or_404

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
    data = AdminBook.objects.all()
    xml_data = serializers.serialize("xml", data)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    data = AdminBook.objects.all()
    json_data = serializers.serialize("json", data)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_id(request, id):
    data = get_object_or_404(AdminBook, pk=id)
    xml_data = serializers.serialize("xml", [data])
    return HttpResponse(xml_data, content_type="application/xml")

def show_json_id(request, id):
    data = get_object_or_404(AdminBook, pk=id)
    json_data = serializers.serialize("json", [data])
    return HttpResponse(json_data, content_type="application/json")