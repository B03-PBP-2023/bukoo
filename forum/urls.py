from django.urls import path
import forum.views as views 

app_name = 'forum'

urlpatterns = [
    path('forum/<int:id>/', views.show_forum, name='show_forum'),
    path('api/forum/get-forum/<int:id>/', views.get_forum_json, name='get_forum_json'),
    path('api/forum/get-reply/<int:id>/', views.get_reply_json, name='get_reply_json'),
    path('api/forum/create-forum-ajax/<int:id>/', views.add_forum_ajax, name='add_forum_ajax'),
    path('api/forum/create-reply-ajax/<int:forum_id>/', views.add_reply_ajax, name='add_reply_ajax'),
    path('api/forum/edit-reply/<int:reply_id>/', views.edit_reply, name='edit_reply'),
    path('api/forum/delete-reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('create-forum-flutter/', views.create_forum_flutter, name='create_forum_flutter'), #update
    path('create-reply-flutter/', views.create_reply_flutter, name='create_reply_flutter'), #update
    path('json-by-user-forum/',views.show_json_by_userForum, name='show_json_by_userForum'), #update
    path('json-by-user-reply/',views.show_json_by_userReply, name='show_json_by_userReply'), #update
]