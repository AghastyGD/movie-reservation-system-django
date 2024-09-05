from django.contrib import admin
from .models import Movie, Genre, Showtime, Seat, Reservation

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    list_filter = ('genre',)
    search_fields = ('title',)

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'formatted_start_time', 'formatted_end_time')
    list_filter = ('movie', 'start_time')
    search_fields = ('movie__title',)
    
    def formatted_start_time(self, obj):
        return obj.formatted_start_time
    formatted_start_time.short_description = 'Start Time'

    def formatted_end_time(self, obj):
        return obj.formatted_end_time
    formatted_end_time.short_description = 'End Time'

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('showtime', 'seat_number', 'is_available')
    list_filter = ('showtime', 'is_available')
    search_fields = ('showtime__movie__title', 'seat_number')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'seat', 'formatted_reservation_time')
    list_filter = ('seat__showtime__movie', 'seat__showtime__start_time')
    search_fields = ('user__username', 'seat__showtime__movie__title')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        summary = self.get_summary_data(qs)
        response.context_data['summary'] = summary

        return response

    def get_summary_data(self, queryset):
        total_reservations = queryset.count()
        total_capacity = Seat.objects.count()

        return {
            'total_reservations': total_reservations,
            'total_capacity': total_capacity,
        }

    def formatted_reservation_time(self, obj):
        return obj.formatted_reservation_time
    formatted_reservation_time.short_description = 'Reservation Time'