from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.core import serializers
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json

from book_collection import utils
from book_collection.models import Book, Genre
from book_collection.form import BookForm

def __create_query(params:dict):
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
  if('keyword' in params):
    keyword = params['keyword']
    fields = ['title', 'author', 'isbn']
    for field in fields:
      query |= Q(**{query_dict[field]:keyword})
  
  # for key, value in params.items():
  #   if(key in query_dict):
  #     query &= Q(**{query_dict[key]:value})
  return query


@require_http_methods(['GET'])
def get_book_list(request):
  FIELDS = ['title', 'image_url', 'author']
  # Get filtered books
  query = __create_query(request.GET)
  books = Book.objects.filter(query).distinct().order_by('id')
  
  # Pagination
  page = request.GET.get('page', 1)
  items_per_page = request.GET.get('items_per_page', 20)
  paginator = Paginator(books, items_per_page)
  books = paginator.get_page(page)
  data = serializers.serialize('json', books, fields=FIELDS, use_natural_foreign_keys=True)

  return JsonResponse(
    {
      'page': page,
      'item_per_page': items_per_page,
      'total_item': paginator.count,
      'total_page': paginator.num_pages,
      'start_index': books.start_index(),
      'end_index': books.end_index(),
      'data': json.loads(data)
    }, 
    safe=False
  )


@require_http_methods(['GET'])
def get_book_detail(request, id):
  book = get_list_or_404(Book, pk=id)
  return HttpResponse(
    serializers.serialize('json', book, use_natural_foreign_keys=True)[1:-1],
    content_type="application/json"
  )


@login_required(login_url='/auth/login/')
@require_http_methods(['POST'])
def add_book(request):
  if not request.user.is_author:
    return HttpResponseForbidden('Author role is required')  
  
  form = BookForm(request.POST)
  if not form.is_valid():
    return HttpResponseBadRequest('Invalid field')
  
  new_book = form.save()

  # Author
  new_book.author.add(request.user.mockauthorprofile) # TODO: integrate with user_profile module

  # Image upload
  if('image' in request.FILES):
    image_name = utils.get_image_name(new_book.pk, new_book.title)
    new_book.image_url = utils.upload_image(request.FILES.get('image'), image_name)

  new_book.save()

  return HttpResponse(
    serializers.serialize('json', [new_book], use_natural_foreign_keys=True)[1:-1],
    content_type="application/json", 
    status=201
  )


@login_required(login_url='/auth/login/')
@require_http_methods(['POST'])
def edit_book(request, id):
  if not request.user.is_author:
    return HttpResponseForbidden('Author role is required')
  
  book = get_object_or_404(Book, pk=id, author=request.user.mockauthorprofile)
  form = BookForm(request.POST, instance=book)
  if not form.is_valid():
    return HttpResponseBadRequest('Invalid field')
  
  book = form.save(commit=False)

  # Update image url
  if('image' in request.FILES):
    image_name = utils.get_image_name(book.pk, book.title)
    book.image_url = utils.edit_image(request.FILES.get('image'), image_name, book.image_url)
    
  book.save()
  form.save_m2m()

  return HttpResponse(
    serializers.serialize('json', [book], use_natural_foreign_keys=True)[1:-1],
    content_type="application/json"
  )


@login_required(login_url='/auth/login/')
@require_http_methods(['DELETE'])
def delete_book(request, id):
  if not request.user.is_author:
    return HttpResponseForbidden('Author role is required')
  
  book = get_object_or_404(Book, pk=id, author=request.user.mockauthorprofile)
  utils.delete_image(utils.get_image_name(book.pk, book.title))
  book.delete()
  return HttpResponse('Deleted')

def get_genres(request):
  genres = Genre.objects.all()
  response = [genre.name for genre in list(genres)]
  return JsonResponse(response, safe=False)

def show_search(request):
  return render(request, 'search.html', {})