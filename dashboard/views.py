from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from kyc.models import KYCProfile
from borrowing.models import BorrowLimit, BorrowTransaction
from scoring.models import Referral


@login_required
def index(request):
    """Main lending dashboard view."""

    user = request.user

    # Get or create KYC profile
    kyc_profile, _ = KYCProfile.objects.get_or_create(user=user)

    # Get or create borrow limit
    borrow_limit, _ = BorrowLimit.objects.get_or_create(user=user)

    # Get recent transactions
    recent_transactions = BorrowTransaction.objects.filter(user=user).order_by('-created_at')[:5]

    # Get referrals made
    referrals_count = Referral.objects.filter(referrer=user).count()

    # Calculate total borrowed
    total_borrowed = BorrowTransaction.objects.filter(
        user=user,
        processed=True,
        status__in=['approved', 'completed']
    ).aggregate(total=Sum('amount_debit'))['total'] or 0

    context = {
        'user': user,
        'kyc_profile': kyc_profile,
        'kyc_level': user.kyc_level,
        'score': user.score,
        'aid_recipient': user.aid_recipient,
        'borrow_limit': borrow_limit,
        'recent_transactions': recent_transactions,
        'referrals_count': referrals_count,
        'total_borrowed': total_borrowed,
    }

    return render(request, 'dashboard/index.html', context)
