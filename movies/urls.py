from django.urls import path
from .views import fetch_movie
from .views import add_review, get_reviews


urlpatterns = [
    path('fetch_movie/<str:title>/', fetch_movie, name='fetch_movie'),
    path("add_review/", add_review, name="add_review"),
    path("get_reviews/<str:title>/", get_reviews, name="get_reviews"),
]
