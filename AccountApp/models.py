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

number_validator = RegexValidator(r'^\d{8}$', 'Phone number must be 8 digits.')
class Doctor(User):
    license_number = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6)])
    phone_number = models.CharField(max_length=8, validators=[number_validator])
    specialities=models.ManyToManyField(Specialty, related_name='doctors')


def date_validator(date):
    if date > timezone.localdate():
        raise ValidationError("Date of birth cannot be in the future.")

class Patient(User):
    national_id = models.CharField(max_length=8, unique=True, validators=[RegexValidator(regex=r'^\d{8}$', message='National ID must be 8 digits.')])
    phone_number = models.CharField(max_length=8, validators=[number_validator])
    date_of_birth = models.DateField(validators=[date_validator])



    