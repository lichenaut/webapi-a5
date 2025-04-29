from django.urls import path
from. import views
from.views import register, login_view

urlpatterns = [
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:pk>/add_review/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]