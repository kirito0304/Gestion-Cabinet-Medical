from django.db import models
from django.core.validators import FileExtensionValidator
from AccountApp.models import Doctor, Patient
from django.utils import timezone
from django.core.exceptions import ValidationError
from typing import cast


class Appointment(models.Model):
    reason = models.TextField(max_length=255)
    prescription = models.FileField(upload_to='prescriptions/', null=True, blank=True, validators=[FileExtensionValidator("pdf")])


    class Status(models.TextChoices):
        Pending = 'Pending','Pending'
        Confirmed = 'Confirmed','Confirmed'
        Cancelled = 'Cancelled','Cancelled'
    status=models.CharField(max_length=25, choices=Status.choices, default=Status.Pending)
    duration_minutes = models.PositiveIntegerField(default=30)  # pyright: ignore[reportArgumentType]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField(blank=False, null=False)
    def clean(self):
        modified_date=self._state.adding or (
            Appointment.objects.filter(
                pk=cast(int, self.pk),
                appointment_date=self.appointment_date,
            ).exists()
        )
        if modified_date and self.appointment_date <= timezone.now():
            raise ValidationError("Appointment date cannot be in the past.")

    class Meta:
        ordering = ['appointment_date']
        constraints = [
            models.UniqueConstraint(fields=['doctor', 'appointment_date'], name='unique_appointment_per_doctor',violation_error_message="This doctor already has an appointment at this date and time.")
        ]

