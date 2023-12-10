from django.urls import path
from .views import show_forum, get_forum_json, get_reply_json, add_forum_ajax, add_reply_ajax

app_name = 'forum'

urlpatterns = [
    path('forum/<int:id>/', show_forum, name='show_forum'),
    path('api/forum/get-forum/<int:id>/', get_forum_json, name='get_forum_json'),
    path('api/forum/get-reply/<int:id>/', get_reply_json, name='get_reply_json'),
    path('api/forum/create-forum-ajax/<int:id>/', add_forum_ajax, name='add_forum_ajax'),
    path('api/forum/create-reply-ajax/<int:forum_id>/', add_reply_ajax, name='add_reply_ajax'),
]