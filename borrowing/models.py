from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class BorrowLimit(models.Model):
    """Determine max borrowable amount based on KYC level and score."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='borrow_limit')
    max_borrow_amount = models.DecimalField(max_digits=10, decimal_places=2, default=20)
    available_borrow = models.DecimalField(max_digits=10, decimal_places=2, default=20)
    is_locked = models.BooleanField(default=True)  # Locked until KYC Level 1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.phone_number} - Max: {self.max_borrow_amount}"

    class Meta:
        db_table = 'borrow_limit'
        verbose_name = 'Borrow Limit'
        verbose_name_plural = 'Borrow Limits'

    def update_available(self):
        """Recalculate available borrow based on transactions."""
        total_borrowed = BorrowTransaction.objects.filter(
            user=self.user,
            processed=True
        ).aggregate(models.Sum('amount_debit'))['amount_debit__sum'] or 0

        self.available_borrow = self.max_borrow_amount - Decimal(str(total_borrowed))
        self.save()


class BorrowTransaction(models.Model):
    """Track all borrow transactions."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('repaid', 'Repaid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_transactions')
    amount_before = models.DecimalField(max_digits=10, decimal_places=2)  # Available before
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)  # Requested amount
    borrow_fee = models.DecimalField(max_digits=10, decimal_places=2)  # Fee amount
    amount_debit = models.DecimalField(max_digits=10, decimal_places=2)  # Amount charged (with fee)
    amount_after = models.DecimalField(max_digits=10, decimal_places=2)  # Available after

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    repaid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount_requested}"

    class Meta:
        db_table = 'borrow_transaction'
        verbose_name = 'Borrow Transaction'
        verbose_name_plural = 'Borrow Transactions'
        ordering = ['-created_at']

    def calculate_fee(self):
        """Calculate fee based on percentage from settings."""
        from django.conf import settings
        fee_percent = getattr(settings, 'BORROW_FEE_PERCENT', 5)
        return Decimal(str(self.amount_requested)) * (Decimal(str(fee_percent)) / Decimal('100'))


class BorrowRepayment(models.Model):
    """Track repayments on borrowed amounts."""

    transaction = models.ForeignKey(BorrowTransaction, on_delete=models.CASCADE, related_name='repayments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    repaid_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Repayment - {self.amount_paid}"

    class Meta:
        db_table = 'borrow_repayment'
        verbose_name = 'Borrow Repayment'
        verbose_name_plural = 'Borrow Repayments'
