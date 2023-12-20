from django.urls import path
from .views import show_forum, get_forum_json, get_reply_json, add_forum_ajax, add_reply_ajax, create_forum_flutter, create_reply_flutter, show_json_by_userForum, show_json_by_userReply, delete_forum_flutter

app_name = 'forum'

urlpatterns = [
    path('forum/<int:id>/', show_forum, name='show_forum'),
    path('api/forum/get-forum/<int:id>/', get_forum_json, name='get_forum_json'),
    path('api/forum/get-reply/<int:id>/', get_reply_json, name='get_reply_json'),
    path('api/forum/create-forum-ajax/<int:id>/', add_forum_ajax, name='add_forum_ajax'),
    path('api/forum/create-reply-ajax/<int:forum_id>/', add_reply_ajax, name='add_reply_ajax'),
    path('create-forum-flutter/', create_forum_flutter, name='create_forum_flutter'), #update
    path('create-reply-flutter/', create_reply_flutter, name='create_reply_flutter'), #update
    path('json-by-user-forum/',show_json_by_userForum, name='show_json_by_userForum'), #update
    path('json-by-user-reply/',show_json_by_userReply, name='show_json_by_userReply'), #update
    path('delete-forum-flutter/<int:forum_id>', delete_forum_flutter, name='delete_forum_flutter'),
]