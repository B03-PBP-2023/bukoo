from django import forms
from django.contrib.auth.forms import UserCreationForm
from auth.models import User

class RegisterForm(UserCreationForm):
  is_author = forms.BooleanField(required=False,widget=forms.Select(choices=[(False, "Reader"), (True, "Author")]), label="Role")

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2', 'is_author')