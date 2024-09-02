from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Showtime, Seat, Reservation

def movie_list(request):
    movies = Movie.objects.all()
    
    context = {
        'movies': movies
    }
    return render(request, "reservations/movie_list.html", context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    showtimes = Showtime.objects.filter(movie=movie)
    
    context = {
        'movie': movie,
        'showtimes': showtimes
    }
    return render(request, 'reservations/movie_detail.html', context)


def reservation_form(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    seats = Seat.objects.filter(showtime=showtime, is_available=True)
    
    if request.method == 'POST':
        seat_id = request.POST.get('seat')
        seat = get_object_or_404(Seat, pk=seat_id)
        reservation = Reservation(user=request.user, seat=seat)
        reservation.save()
        return redirect('movie_list')
    
    context = {
        'showtime': showtime,
        'seats': seats
    }
    
    return render(request, 'reservations/reservation_form.html', context)