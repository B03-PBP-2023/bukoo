# from django import forms
# from admin_dashboard.models import BookData

# class BookDataForm(forms.ModelForm):
#     class Meta:
#         model = BookData
#         fields = [
#             'title',
#             'description',
#             'genres',
#             'publisher',
#             'language',
#             'isbn',
#             'num_pages',
#             'publish_date',
#         ]
from django import forms
from .models import AdminBook

class BookDataForm(forms.ModelForm):
    class Meta:
        model = AdminBook
        fields = '__all__'
