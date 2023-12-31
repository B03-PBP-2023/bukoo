from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from auth.forms import RegisterForm
from user_profile.models import Profile
from user_profile.forms import ProfileForm


@csrf_exempt
@require_http_methods(["GET", "POST"])
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user=user)
            return JsonResponse({'status': 'success', 'message': 'Logged In', 'data': {
                'username': user.username,
                'email': user.email,
                'is_author': user.is_author,
                'is_admin': user.is_admin,
                'name': profile.name,
                'profile_id': profile.pk,
            }}, status=200)
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid username or password'}, status=401)

    return render(request, 'login.html')


@csrf_exempt
@require_http_methods(["GET", "POST"])
def register(request):
    form = RegisterForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.is_staff = user.is_admin
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return JsonResponse({'status': 'success', 'message': 'Registered'}, status=201)
        else:
            return JsonResponse({'status': 'failed', 'message': {**form.errors, **profile_form.errors}}, status=400)

    context = {'form': form}
    return render(request, 'register.html', context)


@csrf_exempt
@login_required(login_url='/auth/login/')
@require_http_methods(["POST"])
def logout_user(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Logged out'}, status=200)
