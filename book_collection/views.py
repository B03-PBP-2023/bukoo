from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.core import serializers
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json

from book_collection import utils
from book_collection.models import Book, Genre
from book_collection.form import BookForm
from admin_dashboard.models import BookSubmission
from user_profile.models import Profile


def __create_query(params: dict):
    query_dict = {
        'title': 'title__icontains',
        'genres': 'genres__name__icontains',
        'publisher': 'publisher__icontains',
        'author': 'author__name__icontains',
        'year': 'publish_date__year',
        'year_after': 'publish_date__year__gte',
        'year_before': 'publish_date__year_lte',
        'language': 'language__icontains',
        'isbn': 'isbn__iexact',
    }
    query = Q()
    # For search
    if ('keyword' in params):
        keyword = params['keyword']
        fields = ['title', 'author', 'isbn']
        for field in fields:
            query |= Q(**{query_dict[field]: keyword})

    for key, value in params.items():
        if (key in query_dict):
            query &= Q(**{query_dict[key]: value})

    return query


def _query_verified_only():
    return (Q(booksubmission__status='verified') | Q(booksubmission__isnull=True))


@csrf_exempt
@cache_page(60)
@require_http_methods(['GET'])
def get_book_list(request):
    FIELDS = ['title', 'image_url', 'author']
    # Get filtered books
    query = __create_query(request.GET) & _query_verified_only()
    books = Book.objects.filter(query).distinct().order_by('id')

    # Pagination
    page = request.GET.get('page', 1)
    items_per_page = request.GET.get('items_per_page', 20)
    paginator = Paginator(books, items_per_page)

    # Check if the requested page exceeds the total number of pages
    if int(page) > paginator.num_pages:
        data = []
    else:
        books = paginator.get_page(page)
        data = serializers.serialize(
            'json', books, fields=FIELDS, use_natural_foreign_keys=True)
        data = json.loads(data)

    return JsonResponse(
        {
            'page': int(page),
            'item_per_page': items_per_page,
            'total_item': paginator.count,
            'total_page': paginator.num_pages,
            'start_index': books.start_index() if len(data) > 0 else 0,
            'end_index': books.end_index() if len(data) > 0 else 0,
            'data': data
        },
        safe=False
    )


@csrf_exempt
@cache_page(60)
@require_http_methods(['GET'])
def get_book_home(request):
    FIELDS = ['title', 'image_url', 'author']
    recommendation = Book.objects.filter(
        _query_verified_only()).order_by('id')[:15]
    new_releases = Book.objects.filter(_query_verified_only()).exclude(
        id__in=recommendation).order_by('-publish_date')[:15]
    indonesian = Book.objects.filter(_query_verified_only()).exclude(id__in=recommendation | new_releases).filter(
        language__icontains='indonesia').order_by('id')[:15]
    english = Book.objects.filter(_query_verified_only()).exclude(id__in=recommendation | new_releases | indonesian).filter(
        language__icontains='english').order_by('id')[:15]
    fiction = Book.objects.filter(_query_verified_only()).exclude(id__in=recommendation | new_releases | indonesian | english).filter(
        genres__name='Fiction').order_by('id')[:15]

    data = {
        'recommendation': json.loads(serializers.serialize('json', recommendation, fields=FIELDS, use_natural_foreign_keys=True)),
        'new_releases': json.loads(serializers.serialize('json', new_releases, fields=FIELDS, use_natural_foreign_keys=True)),
        'indonesian': json.loads(serializers.serialize('json', indonesian, fields=FIELDS, use_natural_foreign_keys=True)),
        'english': json.loads(serializers.serialize('json', english, fields=FIELDS, use_natural_foreign_keys=True)),
        'fiction': json.loads(serializers.serialize('json', fiction, fields=FIELDS, use_natural_foreign_keys=True)),
    }

    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(['GET'])
def get_book_detail(request, id):
    book = get_list_or_404(Book, pk=id)
    return HttpResponse(
        serializers.serialize(
            'json', book, use_natural_foreign_keys=True)[1:-1],
        content_type="application/json"
    )


@csrf_exempt
@login_required(login_url='/auth/login/')
@require_http_methods(['POST'])
def add_book(request):
    if not request.user.is_author:
        return HttpResponseForbidden('Author role is required')

    form = BookForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest('Invalid field')

    new_book = form.save()

    genres = request.POST.get('genres')
    if genres != None:
        genres = genres.split(',')
        for genre in genres:
            try:
                genre_obj, created = Genre.objects.update_or_create(name=genre)
                new_book.genres.add(genre_obj)
            except:
                pass

    # Author
    authors = request.POST.get('author')
    if authors != None:
        authors = json.loads(authors)
        for author in authors:
            try:
                author_obj, created = Profile.objects.update_or_create(
                    name=author)
                new_book.author.add(author_obj)
            except:
                pass

    # Image upload
    if ('image' in request.FILES):
        image_name = utils.get_image_name(new_book.pk, new_book.title)
        new_book.image_url = utils.upload_image(
            request.FILES.get('image'), image_name)

    new_book.save()

    book_submission = BookSubmission.objects.create(
        book=new_book, status='pending')

    return HttpResponse(
        serializers.serialize(
            'json', [new_book], use_natural_foreign_keys=True)[1:-1],
        content_type="application/json",
        status=201
    )


@csrf_exempt
@login_required(login_url='/auth/login/')
@require_http_methods(['POST'])
def edit_book(request, id):
    if not request.user.is_author:
        return HttpResponseForbidden('Author role is required')

    book = get_object_or_404(
        Book, pk=id, author=request.user.mockauthorprofile)
    form = BookForm(request.POST, instance=book)
    if not form.is_valid():
        return HttpResponseBadRequest('Invalid field')

    book = form.save(commit=False)

    genres = request.POST.get('genres')
    if genres != None:
        book.genres.clear()
        genres = genres.split(',')
        for genre in genres:
            try:
                genre_obj, created = Genre.objects.update_or_create(name=genre)
                book.genres.add(genre_obj)
            except:
                pass

    # Author
    authors = request.POST.get('author')
    if authors != None:
        authors = json.loads(authors)
        book.author.clear()
        for author in authors:
            try:
                author_obj, created = Profile.objects.update_or_create(
                    name=author)
                book.author.add(author_obj)
            except:
                pass

    # Update image url
    if ('image' in request.FILES):
        image_name = utils.get_image_name(book.pk, book.title)
        book.image_url = utils.edit_image(
            request.FILES.get('image'), image_name, book.image_url)

    book.save()
    form.save_m2m()

    return HttpResponse(
        serializers.serialize(
            'json', [book], use_natural_foreign_keys=True)[1:-1],
        content_type="application/json"
    )


@csrf_exempt
@login_required(login_url='/auth/login/')
@require_http_methods(['DELETE'])
def delete_book(request, id):
    if not request.user.is_author:
        return HttpResponseForbidden('Author role is required')

    book = get_object_or_404(
        Book, pk=id, author=request.user.mockauthorprofile)
    utils.delete_image(utils.get_image_name(book.pk, book.title))
    book.delete()
    return HttpResponse('Deleted')


@csrf_exempt
@cache_page(60)
def get_genres(request):
    genres = Genre.objects.all()
    response = [genre.name for genre in list(genres)]
    return JsonResponse(response, safe=False)


@csrf_exempt
@cache_page(60)
def get_authors(request):
    # filter only author
    authors = Profile.objects.annotate(
        num_books=Count('book')).filter(num_books__gt=0)
    response = [author.name for author in list(authors)]
    return JsonResponse(response, safe=False)


def show_search(request):
    return render(request, 'search.html', {})


def show_book_detail(request, slug: str):
    return render(request, 'book-detail.html', {})


def show_book_submission(request):
    return render(request, 'book-submission.html', {})


def show_landing_page(request):
    return render(request, 'index.html', {})
