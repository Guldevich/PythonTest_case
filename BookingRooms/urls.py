from django.urls import path
from BookingRooms import views
from django.contrib import admin

urlpatterns = [
    path('rooms/', views.room_list, name='room_list'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
