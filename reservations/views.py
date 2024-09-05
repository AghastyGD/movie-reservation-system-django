from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Movie, Showtime, Seat, Reservation

def home(request):
    context = {
        'movies': Movie.objects.all()
    }
    return render(request, 'home.html', context)

def movie_list(request):
    context = {
        'movies': Movie.objects.all()
    }
    return render(request, "reservations/movie_list.html", context)

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    context = {
        'movie': movie,
        'showtimes': Showtime.objects.filter(movie=movie)
    }
    return render(request, 'reservations/movie_detail.html', context)

@login_required
def reservation_form(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    seats = Seat.objects.filter(showtime=showtime)
    context = {
        'showtime': showtime,
        'seats': seats
    }
    
    if request.method == 'POST':
        seat_ids = request.POST.getlist('seats')
        if not seat_ids:
            messages.error(request, "Please select at least one seat.")
            return render(request, 'reservations/reservation_form.html', context)
        
        unavailable_seats = []
        for seat_id in seat_ids:
            seat = get_object_or_404(Seat, pk=seat_id)
            if not seat.is_available:
                unavailable_seats.append(seat.seat_number)
        
        if unavailable_seats:
            messages.error(request, f"Seats {', '.join(unavailable_seats)} are no longer available.")
            return render(request, 'reservations/reservation_form.html', context)
        
        for seat_id in seat_ids:
            seat = get_object_or_404(Seat, pk=seat_id)
            Reservation.objects.create(user=request.user, seat=seat)
        
        messages.success(request, "Seats reserved successfully!")
        return redirect('movie_list')
    
    return render(request, 'reservations/reservation_form.html', context)

@login_required
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-reservation_time')
    context = {
        'reservations': reservations
    }
    return render(request, 'reservations/user_reservations.html', context)

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.user == reservation.user and reservation.is_upcoming:
        reservation.delete()
        messages.success(request, "Your reservation has been successfully cancelled.")
    else:
        messages.error(request, "Unable to cancel the reservation.")
    return redirect(reverse('user_reservations'))