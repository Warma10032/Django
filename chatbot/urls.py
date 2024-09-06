from django.urls import path

from chatbot.views import view, chat,knowledge

urlpatterns=[
    path('',view.login, name='login'),
    path('users/', view.user_list, name='user_list'),
    path('user/create/', view.user_create, name='user_create'),
    path('users/update/<int:pk>/', view.user_update, name='user_update'),
    path('users/delete/<int:pk>/', view.user_delete, name='user_delete'),
    path('chat/', chat.grodio_chat_view, name='chat_view'),
    path('build_knowledge/', knowledge.build_knowledge_view, name='build_knowledge_view'),
    path('choice/', view.choice_view, name='choice_view')

]