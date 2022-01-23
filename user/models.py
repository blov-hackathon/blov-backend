from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid
from config.ethereum import create_wallet


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, phone_number, name, blood_type, password):
        wallet = create_wallet()
        user = self.model(phone_number=phone_number,
                          name=name, blood_type=blood_type, private_key=wallet.privateKey.hex(), address=wallet.address)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, blood_type, password):
        wallet = create_wallet()
        user = self.model(phone_number=phone_number,
                          name=name, blood_type=blood_type, private_key=wallet.privateKey.hex(), address=wallet.address)
        user.set_password(password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    BLOOD_TYPE_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    name = models.CharField(max_length=5, blank=False,
                            null=False, unique=False)
    phone_number = models.CharField(
        max_length=11, blank=False, null=False, unique=True)
    blood_type = models.CharField(
        max_length=3, blank=False, choices=BLOOD_TYPE_CHOICES, null=False, unique=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    private_key = models.CharField(max_length=200, unique=True, null=True)
    address = models.CharField(max_length=200, unique=True, null=True)

    REQUIRED_FIELDS = ['blood_type', 'name']
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.phone_number = self.phone_number.replace('-', '')
        super().save(*args, **kwargs)


class AuthToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    user = models.ForeignKey(
        User, related_name='auth_tokens', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.id}"
