from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin,BaseUserManager

ROLE_CHOICES = [
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
]

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser,PermissionsMixin):
    username = models.CharField(max_length=255,unique=False,null=False)
    email = models.EmailField(unique=True, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    reservations = models.ManyToManyField('Appointment', related_name='reserving_users', blank=True)
    appointments = models.ManyToManyField('Appointment', related_name='appointed_users', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

class Appointment(models.Model):
    date = models.DateField(null=False)
    time = models.TimeField(null=False,unique=True)
    is_reserved = models.BooleanField(default=False)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments', null=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
