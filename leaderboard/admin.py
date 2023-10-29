from django.contrib import admin
from .models import Leaderboard
# Register your models here.


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['book', 'userProfile', 'is_recommended', 'created_at']
