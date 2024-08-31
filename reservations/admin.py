from django.contrib import admin
from .models import Movie, Genre, Showtime, Seat, Reservation

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'formatted_start_time', 'formatted_end_time')

    def formatted_start_time(self, obj):
        return obj.formatted_start_time
    formatted_start_time.short_description = 'Start Time'

    def formatted_end_time(self, obj):
        return obj.formatted_end_time
    formatted_end_time.short_description = 'End Time'
    

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('showtime', 'seat_number', 'is_available')
    
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'seat', 'formatted_reservation_time')
    
    def formatted_reservation_time(self, obj):
        return obj.formatted_reservation_time
    formatted_reservation_time.short_description = 'Reservation Time'
    