from django.db import models
from django.contrib.auth.models import User  # so we can get a reference of who's logged in and rated the movie
from django.core.validators import MaxValueValidator, \
    MinValueValidator  # use to validate that the rating is within the max and min


class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_rating(self):
        ratings = Rating.objects.filter(movie=self)
        sum = 0
        for rating in ratings:
            sum += rating.stars
        if len(ratings) > 0:
            avg_rating = sum/len(ratings)
            return avg_rating
        else:
            return 0


class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='movie', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'movie'),)  # users cannot rate movies more than once
        index_together = (('user', 'movie'),)


