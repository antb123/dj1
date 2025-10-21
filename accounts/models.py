from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager where phone_number is the unique identifier."""

    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a regular user with the given phone_number and password."""
        if not phone_number:
            raise ValueError(_('The Phone Number field must be set'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """Create and save a superuser with the given phone_number and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with phone_number as the primary identifier for WhatsApp OTP auth."""

    username = None  # Remove username field
    email = None  # Remove email field
    phone_number = models.CharField(_('phone number'), max_length=20, unique=True, default='')

    # KYC and Lending Fields
    kyc_level = models.IntegerField(default=0, choices=[(0, 'None'), (1, 'Level 1'), (2, 'Level 2')])
    score = models.IntegerField(default=0)
    aid_recipient = models.BooleanField(default=True)

    # Storage fields (kept for backward compatibility)
    storage_quota = models.BigIntegerField(default=1024*1024*1024)  # 1GB default
    storage_used = models.BigIntegerField(default=0)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def get_storage_percentage(self):
        """Calculate storage usage percentage."""
        if self.storage_quota == 0:
            return 0
        return (self.storage_used / self.storage_quota) * 100

    def has_storage_available(self, file_size):
        """Check if user has enough storage for a new file."""
        return (self.storage_used + file_size) <= self.storage_quota

    def update_storage_used(self):
        """Recalculate storage used based on uploaded documents."""
        # Documents app removed - this is kept for legacy compatibility
        self.storage_used = 0
        self.save(update_fields=['storage_used'])
