from django.forms import ModelForm
from book_collection.models import Book

class BookForm(ModelForm):
  class Meta:
    model = Book
    fields = [
      'title', 
      'description', 
      'publisher',
      'language',
      'isbn',
      'num_pages',
      'publish_date',
    ]