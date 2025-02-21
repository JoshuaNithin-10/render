import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from django.db import models

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

class Movie(models.Model):
    title = models.CharField(max_length=255)
    imdb_id = models.CharField(max_length=50, unique=True)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=255)
    imdb_rating = models.FloatField()

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.CharField(max_length=100)  # Username
    rating = models.IntegerField()
    review_text = models.TextField()
    sentiment_score = models.FloatField(null=True, blank=True)  # AI sentiment analysis

    def save(self, *args, **kwargs):
        self.sentiment_score = sia.polarity_scores(self.review_text)['compound']
        super().save(*args, **kwargs)    
    def __str__(self):
        return f"{self.user} - {self.movie.title}"
