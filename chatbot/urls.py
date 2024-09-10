from django.urls import path

from chatbot.views import view, chat,knowledge
from chatbot.views import knowledge

urlpatterns=[
    path('',view.login, name='login'),
    path('users/', view.user_list, name='user_list'),
    path('user/create/', view.user_create, name='user_create'),
    path('users/update/<int:pk>/', view.user_update, name='user_update'),
    path('users/delete/<int:pk>/', view.user_delete, name='user_delete'),
    path('register/',view.register),
    path('upload/', knowledge.build_knowledge_view, name='upload_file'),
    path('files/', knowledge.list_uploaded_files, name='list_files'),
    path('files/<str:filename>/', knowledge.delete_file, name='delete_file'),
    path('view_file/<str:filename>/', knowledge.view_uploaded_file_view, name='view_uploaded_file'),

]