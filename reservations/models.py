from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from .utils.datetime_utils import format_datetime

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
    
class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    num_seats = models.PositiveIntegerField(default=100) 

    def __str__(self):
        return f"{self.movie.title} - {self.formatted_start_time}"
    
    @property
    def formatted_start_time(self):
        return format_datetime(self.start_time)

    @property
    def formatted_end_time(self):
        return format_datetime(self.end_time)
    
    def save(self, *args, **kwargs):
        creating = self.pk is None 
        super().save(*args, **kwargs)
        if creating:
            self.create_seats()

    def create_seats(self):
        for i in range(1, self.num_seats + 1):
            Seat.objects.create(showtime=self, seat_number=f"Seat {i}")
    
class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True) 
    
    def __str__(self):
        return f"Seat {self.seat_number} for Showtime {self.showtime}"
    
class Reservation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reservation by {self.user} for seat {self.seat} at {self.formatted_reservation_time}"
    
    @property
    def formatted_reservation_time(self):
        return format_datetime(self.reservation_time)
    
    def save(self, *args, **kwargs):
        if not self.seat.is_available:
            raise ValidationError("This seat is already reserved.")
        self.seat.is_available = False
        self.seat.save()
        super().save(*args, **kwargs)


