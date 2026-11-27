from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    pass
class Specialty(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta():
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"
        

number_validator = RegexValidator(r'^\d{8}$', 'Phone number must be 8 digits.')
class Doctor(User):
    license_number = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6)])
    phone_number = models.CharField(max_length=8, validators=[number_validator])
    specialities=models.ManyToManyField(Specialty, related_name='doctors')
    
    class Meta():
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.license_number}"


def date_validator(date):
    if date > timezone.localdate():
        raise ValidationError("Date of birth cannot be in the future.")

class Patient(User):
    national_id = models.CharField(max_length=8, unique=True, validators=[RegexValidator(regex=r'^\d{8}$', message='National ID must be 8 digits.')])
    phone_number = models.CharField(max_length=8, validators=[number_validator])
    date_of_birth = models.DateField(validators=[date_validator])
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.national_id}"



    