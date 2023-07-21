from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Room, Booking
from datetime import date


def is_room_available(room_id, check_in_date, check_out_date) -> bool:
    try:
        room = Room.objects.get(id=room_id)
        bookings = Booking.objects.filter(
            room=room,
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        )
        return not bookings.exists()
    except Room.DoesNotExist:
        return False


def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
    except Booking.DoesNotExist:
        pass
    return redirect('booking_list')


def home(request) -> str:
    return render(request, 'main/home.html')


def room_list(request) -> str:
    price_filter = request.GET.get('price')
    capacity_filter = request.GET.get('capacity')
    check_in_date = request.GET.get('check_in_date', date.today())
    check_out_date = request.GET.get('check_out_date')
    sort_by = request.GET.get('sort')

    rooms = Room.objects.all()
    if price_filter:
        rooms = rooms.filter(price_per_day__lte=price_filter)
    if capacity_filter:
        rooms = rooms.filter(capacity__gte=capacity_filter)

    if check_out_date and check_in_date:
        for room in rooms:
            room.available = is_room_available(room.id, check_in_date, check_out_date)

    if sort_by:
        if sort_by == 'price_asc':
            rooms = rooms.order_by('price_per_day')
        elif sort_by == 'price_desc':
            rooms = rooms.order_by('-price_per_day')
        elif sort_by == 'capacity_asc':
            rooms = rooms.order_by('capacity')
        elif sort_by == 'capacity_desc':
            rooms = rooms.order_by('-capacity')

    return render(request, 'main/room_list.html', {
        'rooms': rooms,
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
        'sort_by': sort_by,
    })


@login_required
def booking_list(request) -> str:
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'main/booking_list.html', {'bookings': bookings})


@login_required
def book_room(request, room_id) -> str:
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        check_in_date = request.POST['check_in_date']
        check_out_date = request.POST['check_out_date']
        booking = Booking(room=room, user=request.user, check_in_date=check_in_date, check_out_date=check_out_date)
        booking.save()
        return redirect('booking_list')
    return render(request, 'main/book_room.html', {'room': room})


def login_view(request) -> str:
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('room_list')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})


def register_view(request) -> str:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('room_list')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
