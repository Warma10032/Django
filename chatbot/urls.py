from django.urls import path

from . import views
urlpatterns=[
    path('',views.login),
    path('users/', views.user_list, name='user_list'),
    path('user/create/', views.user_create, name='user_create'),
    path('users/update/<int:pk>/', views.user_update, name='user_update'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),
]