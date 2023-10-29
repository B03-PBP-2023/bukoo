from django.shortcuts import render
from admin_dashboard.models import AdminBook
from django.http import JsonResponse

def get_book_list(request):
    books = AdminBook.objects.all()
    book_data = [
        {
            'title': book.title,
            'description': book.description,
            'genres': book.genres,
            'publisher': book.publisher,
            'language': book.language,
            'isbn': book.isbn,
            'num_pages': book.num_pages,
            'publish_date': book.publish_date.strftime("%Y-%m-%d") if book.publish_date else None
        }
        for book in books
    ]
    return JsonResponse(book_data, safe=False)

def admin_dashboard(request):
    return render(request, 'admin.html')


