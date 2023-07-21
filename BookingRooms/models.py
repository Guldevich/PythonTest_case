from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=100)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()

    def is_available(self, check_in_date, check_out_date):
        try:
            bookings = self.booking_set.filter(
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            )
            return not bookings.exists()
        except Booking.DoesNotExist:
            return True


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()


