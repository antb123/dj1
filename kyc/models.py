from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class KYCProfile(models.Model):
    """User KYC profile and verification status."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kyc_profile')

    # Level 1 - Questionnaire data
    full_name = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=200, blank=True)
    mobile_money_number = models.CharField(max_length=50, blank=True)
    id_type = models.CharField(max_length=50, blank=True)
    id_number = models.CharField(max_length=100, blank=True)

    has_business = models.BooleanField(null=True)
    is_only_owner = models.BooleanField(null=True)
    business_description = models.TextField(blank=True)
    loan_purpose = models.TextField(blank=True)

    # Questionnaire completion
    all_questions_answered = models.BooleanField(default=False)
    level_1_completed_at = models.DateTimeField(null=True, blank=True)

    # Level 2 - Documents
    business_registration_doc = models.FileField(upload_to='kyc/documents/', null=True, blank=True)
    electricity_bill_doc = models.FileField(upload_to='kyc/documents/', null=True, blank=True)
    level_2_completed_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KYC - {self.user.phone_number}"

    class Meta:
        db_table = 'kyc_profile'
        verbose_name = 'KYC Profile'
        verbose_name_plural = 'KYC Profiles'

    @property
    def unique_identifier(self):
        """Generate unique KYC identifier: WhatsApp + DOB + ID Number"""
        if self.date_of_birth and self.id_number:
            dob_str = self.date_of_birth.strftime('%d%m%Y')
            return f"{self.user.phone_number}_{dob_str}_{self.id_number}"
        return None


class QuestionnaireResponse(models.Model):
    """Track user responses to questionnaire questions."""

    kyc_profile = models.ForeignKey(KYCProfile, on_delete=models.CASCADE, related_name='responses')
    question_index = models.IntegerField()  # 0-9 for the 10 questions
    question_text = models.TextField()
    answer = models.TextField()
    answered_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.kyc_profile.user.phone_number} - Q{self.question_index + 1}"

    class Meta:
        db_table = 'questionnaire_response'
        unique_together = ('kyc_profile', 'question_index')
        verbose_name = 'Questionnaire Response'
        verbose_name_plural = 'Questionnaire Responses'


class KYCDocument(models.Model):
    """Store additional documents for KYC Level 2."""

    DOCUMENT_TYPES = [
        ('business_registration', 'Business Registration'),
        ('electricity_bill', 'Electricity Bill'),
        ('national_id', 'National ID'),
        ('other', 'Other'),
    ]

    kyc_profile = models.ForeignKey(KYCProfile, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='kyc/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_kyc_documents')
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.kyc_profile.user.phone_number} - {self.get_document_type_display()}"

    class Meta:
        db_table = 'kyc_document'
        verbose_name = 'KYC Document'
        verbose_name_plural = 'KYC Documents'
