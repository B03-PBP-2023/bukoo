from django.forms import ModelForm
from user_profile.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "gender", "about_user", "date_of_birth", "prefered_genre", "profile_picture"]

