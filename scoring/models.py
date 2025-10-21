from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ScoreLog(models.Model):
    """Track all score changes for a user."""

    REASON_CHOICES = [
        ('referral', 'User Referral'),
        ('phone_bill', 'Phone Bill Upload'),
        ('admin_adjustment', 'Admin Adjustment'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score_logs')
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    points_added = models.IntegerField()
    previous_score = models.IntegerField()
    new_score = models.IntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.get_reason_display()} (+{self.points_added})"

    class Meta:
        db_table = 'score_log'
        verbose_name = 'Score Log'
        verbose_name_plural = 'Score Logs'
        ordering = ['-created_at']


class PhoneBillUpload(models.Model):
    """Track phone bill uploads for scoring."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone_bill_uploads')
    phone_bill_file = models.FileField(upload_to='score/phone_bills/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_phone_bills')
    verified_at = models.DateTimeField(null=True, blank=True)
    score_awarded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.phone_number} - Phone Bill"

    class Meta:
        db_table = 'phone_bill_upload'
        verbose_name = 'Phone Bill Upload'
        verbose_name_plural = 'Phone Bill Uploads'


class Referral(models.Model):
    """Track referrals and scoring."""

    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_made')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_received', null=True, blank=True)
    referral_code = models.CharField(max_length=50, unique=True)
    referred_phone = models.CharField(max_length=20)  # Phone of referred person
    score_awarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.phone_number} -> {self.referred_phone}"

    class Meta:
        db_table = 'referral'
        verbose_name = 'Referral'
        verbose_name_plural = 'Referrals'
        ordering = ['-created_at']

    @staticmethod
    def generate_referral_code(user):
        """Generate unique referral code."""
        import hashlib
        import uuid
        data = f"{user.phone_number}_{uuid.uuid4()}"
        return hashlib.md5(data.encode()).hexdigest()[:8]


class ScoreRule(models.Model):
    """Configurable scoring rules."""

    rule_name = models.CharField(max_length=100, unique=True)
    rule_type = models.CharField(
        max_length=50,
        choices=[
            ('referral', 'Referral'),
            ('phone_bill', 'Phone Bill'),
            ('kyc_level_1', 'KYC Level 1'),
            ('kyc_level_2', 'KYC Level 2'),
            ('other', 'Other'),
        ]
    )
    points_value = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rule_name} - {self.points_value} pts"

    class Meta:
        db_table = 'score_rule'
        verbose_name = 'Score Rule'
        verbose_name_plural = 'Score Rules'
