from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('reservation/<int:showtime_id>/', views.reservation_form, name='reservation_form'),    
    path('reservations/', views.user_reservations, name='user_reservations'),
    path('reservations/cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]
