from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# Create your models here.

class UserManager(BaseUserManager):
    """
    manager user model
    """

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('شماره تلفن ارائه نشده است')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('کاربر ارشد باید دارای مقدار is_staff=True باشد.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('کاربر ارشد باید دارای مقدار is_SuperUser=True باشد.')
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model from base
    """
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره')
    first_name = models.CharField(max_length=55, null=True, blank=True, verbose_name='اسم')
    last_name = models.CharField(max_length=55, null=True, blank=True, verbose_name='فامیل')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)

    manager = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ["first_name", 'last_name']

    def __str__(self):
        return f"{self.phone} {self.first_name}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["-created_at"]),
        ]


class AddressUser(models.Model):
    """
    User address model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name="کاربر")
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name="شماره")
    first_name = models.CharField(max_length=55, verbose_name='اسم', null=True, blank=True)
    last_name = models.CharField(max_length=55, verbose_name='فامیل', null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True, verbose_name="استان")
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name="شهر")
    cod_post = models.CharField(max_length=10, null=True, blank=True, verbose_name="کد پستی")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["-created_at"]),
        ]


class OTPCode(models.Model):
    """
    The model stores the code sent to the user for validation that the user has requested to login or...
    """
    phone = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def create_code(cls, phone, code, minuter_valid=2):
        return cls.objects.create(phone=phone, code=code,
                                  expires_at=timezone.now() + timedelta(minutes=minuter_valid))

    def __str__(self):
        return f"{self.phone} - {self.code}"
