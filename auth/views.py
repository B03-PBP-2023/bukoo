from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from auth.forms import RegisterForm
from user_profile.models import Profile

@require_http_methods(["GET", "POST"])
def login_user(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return JsonResponse({'message': 'Logged In'}, status=200)
    else:
      return JsonResponse({'message': 'Invalid credential'}, status=401)
  
  return render(request, 'login.html')
  


@require_http_methods(["GET", "POST"])  
def register(request):
  form = RegisterForm(request.POST or None)
  if request.method == "POST":
    if form.is_valid():
      user = form.save()
      Profile.objects.create(user=user)
      return JsonResponse({'message': 'Registered'}, status=201)
    else:
      return JsonResponse({'message': form.errors}, status=400)
    
  context = {'form': form}
  return render(request, 'register.html', context)

@csrf_exempt
@login_required(login_url='/auth/login/')
@require_http_methods(["POST"])  
def logout_user(request):
  logout(request)
  return JsonResponse({'message': 'Logged out'}, status=200)