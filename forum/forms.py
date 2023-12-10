from django import forms
from django.forms import ModelForm
from forum.models import ForumDiscuss

class ForumForm(ModelForm):
    class Meta:
        model = ForumDiscuss
        fields = ["subject", "description"]
        widget = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            }