from django.shortcuts import render

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Movie, Review


API_KEY = "6df842f5ba4f78f7b615bad29b21f406"  # Get from https://www.themoviedb.org/

@csrf_exempt
def fetch_movie(request, title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    response = requests.get(url).json()

    if response['results']:
        movie_data = response['results'][0]
        movie, created = Movie.objects.get_or_create(
            imdb_id=movie_data['id'],
            defaults={
                "title": movie_data["title"],
                "release_year": movie_data["release_date"].split("-")[0],
                "genre": ", ".join(genre["name"] for genre in movie_data.get("genres", [])),
                "imdb_rating": movie_data.get("vote_average", 0),
            }
        )
        return JsonResponse({"success": True, "movie": movie_data})
    
    return JsonResponse({"success": False, "message": "Movie not found"})
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        movie_title = data.get("movie")
        user = data.get("user")
        rating = data.get("rating")
        review_text = data.get("review_text")

        try:
            movie = Movie.objects.get(title=movie_title)
        except Movie.DoesNotExist:
            return JsonResponse({"success": False, "message": "Movie not found"}, status=404)

        review = Review.objects.create(movie=movie, user=user, rating=rating, review_text=review_text)
        return JsonResponse({"success": True, "message": "Review added", "sentiment": review.sentiment_score})
    
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


def get_reviews(request, title):
    try:
        movie = Movie.objects.get(title=title)
        reviews = movie.reviews.all().values("user", "rating", "review_text", "sentiment_score")
        return JsonResponse({"success": True, "reviews": list(reviews)})
    except Movie.DoesNotExist:
        return JsonResponse({"success": False, "message": "Movie not found"}, status=404)