from django.shortcuts import render
from admin_dashboard.models import BookSubmission
from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponseRedirect
# from author.forms import ProductForm
from django.urls import reverse


# @login_required(login_url='/login')

def show_verif(request):
    context = {
        'author': 'fayya',
        'title': 'kalkulus 1',
        'genre' : 'romantic',
        'description' : 'pusing',
    }
    return render(request, "admin.html", context)



# def show_xml(request):
#     data = BookSubmission.objects.all()
#     return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# def show_json(request):
#     data = BookSubmission.objects.all()
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# def show_xml_by_id(request, id):
#     data = BookSubmission.objects.filter(pk=id)
#     return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# def show_json_by_id(request, id):
#     data = BookSubmission.objects.filter(pk=id)
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# def get_book_json(request):
#     books = BookSubmission.objects.all()
#     data = serializers.serialize("json", books)
#     return HttpResponse(data, content_type="application/json")

# Create your views here.
