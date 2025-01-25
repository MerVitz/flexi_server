from django.utils import timezone
from django.core.mail import send_mail
from .models import Booking, Notification

def send_reminder_notifications():
    upcoming_bookings = Booking.objects.filter(
        start_time__gte=timezone.now(),
        start_time__lt=timezone.now() + timezone.timedelta(days=1),
        is_confirmed=True
    )

    for booking in upcoming_bookings:
        Notification.objects.create(
            user=booking.user,
            message=f"Reminder: Your booking for {booking.equipment.name} starts soon.",
            requires_confirmation=True
        )
        send_mail(
            'Booking Reminder',
            f"Dear {booking.user.email},\n\nYour booking for {booking.equipment.name} starts soon. Please confirm your attendance by clicking the link: http://yourapp.com/confirm_booking/{booking.id}",
            'admin@example.com',
            [booking.user.email],
            fail_silently=False,
        )
