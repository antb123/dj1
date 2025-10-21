from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
import string

User = get_user_model()


class WhatsAppUser(models.Model):
    """Track WhatsApp users and their verification status."""

    phone_number = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='whatsapp_profile')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {'Verified' if self.is_verified else 'Unverified'}"

    class Meta:
        db_table = 'whatsapp_user'
        verbose_name = 'WhatsApp User'
        verbose_name_plural = 'WhatsApp Users'


class OTP(models.Model):
    """Store OTP for phone number verification."""

    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.phone_number}"

    class Meta:
        db_table = 'otp'
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'
        ordering = ['-created_at']

    @staticmethod
    def generate_code():
        """Generate a random 6-digit OTP code."""
        return ''.join(random.choices(string.digits, k=6))

    @staticmethod
    def generate_expiry():
        """Generate expiry time (5 minutes from now)."""
        from django.conf import settings
        duration = getattr(settings, 'OTP_VALID_DURATION', 300)
        return timezone.now() + timezone.timedelta(seconds=duration)

    def is_expired(self):
        """Check if OTP has expired."""
        return timezone.now() > self.expires_at

    def is_valid_attempt(self):
        """Check if OTP still has valid attempts remaining."""
        from django.conf import settings
        max_attempts = getattr(settings, 'OTP_MAX_ATTEMPTS', 3)
        return self.attempts < max_attempts

    def increment_attempts(self):
        """Increment attempt counter."""
        self.attempts += 1
        self.save()
