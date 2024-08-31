from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    poster_image = models.ImageField(upload_to="movie_poster/")
    genre = models.ManyToManyField(Genre)
    
    def __str__(self):
        return self.title

