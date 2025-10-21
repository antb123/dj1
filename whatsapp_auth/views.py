from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.conf import settings
import json

from .models import OTP, WhatsAppUser

User = get_user_model()


class RequestOTPView(View):
    """Handle OTP request for phone number."""

    def get(self, request):
        """Display phone number input form."""
        return render(request, 'whatsapp_auth/request_otp.html')

    def post(self, request):
        """Generate and send OTP."""
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request
            try:
                data = json.loads(request.body)
                phone_number = data.get('phone_number', '').strip()

                if not phone_number:
                    return JsonResponse({'success': False, 'error': 'Phone number required'})

                # Generate OTP
                otp_code = OTP.generate_code()
                otp_expiry = OTP.generate_expiry()

                # Delete old OTPs for this number
                OTP.objects.filter(phone_number=phone_number, is_used=False).delete()

                # Create new OTP
                otp = OTP.objects.create(
                    phone_number=phone_number,
                    code=otp_code,
                    expires_at=otp_expiry
                )

                # TODO: Send OTP via Twilio WhatsApp
                # For now, log to console
                print(f"\n[OTP] Phone: {phone_number}, Code: {otp_code}")

                # Store phone in session for next step
                request.session['phone_number'] = phone_number

                return JsonResponse({
                    'success': True,
                    'message': 'OTP sent to WhatsApp',
                    'redirect': 'whatsapp_auth:verify_otp'
                })

            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        # Regular form submission
        phone_number = request.POST.get('phone_number', '').strip()

        if not phone_number:
            return render(request, 'whatsapp_auth/request_otp.html', {'error': 'Phone number required'})

        # Generate OTP
        otp_code = OTP.generate_code()
        otp_expiry = OTP.generate_expiry()

        # Delete old OTPs
        OTP.objects.filter(phone_number=phone_number, is_used=False).delete()

        # Create new OTP
        otp = OTP.objects.create(
            phone_number=phone_number,
            code=otp_code,
            expires_at=otp_expiry
        )

        # TODO: Send OTP via Twilio WhatsApp
        print(f"\n[OTP] Phone: {phone_number}, Code: {otp_code}")

        request.session['phone_number'] = phone_number
        return redirect('whatsapp_auth:verify_otp')


class VerifyOTPView(View):
    """Handle OTP verification."""

    def get(self, request):
        """Display OTP verification form."""
        phone_number = request.session.get('phone_number')

        if not phone_number:
            return redirect('whatsapp_auth:request_otp')

        return render(request, 'whatsapp_auth/verify_otp.html', {'phone_number': phone_number})

    def post(self, request):
        """Verify OTP and create/login user."""
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request
            try:
                data = json.loads(request.body)
                otp_code = data.get('otp_code', '').strip()
                phone_number = request.session.get('phone_number')

                if not phone_number or not otp_code:
                    return JsonResponse({'success': False, 'error': 'Missing data'})

                # Get latest OTP for this phone
                otp = OTP.objects.filter(
                    phone_number=phone_number,
                    is_used=False
                ).order_by('-created_at').first()

                if not otp:
                    return JsonResponse({'success': False, 'error': 'No OTP found. Request a new one.'})

                if otp.is_expired():
                    return JsonResponse({'success': False, 'error': 'OTP expired'})

                if not otp.is_valid_attempt():
                    return JsonResponse({'success': False, 'error': 'Too many attempts'})

                if otp.code != otp_code:
                    otp.increment_attempts()
                    return JsonResponse({'success': False, 'error': 'Invalid OTP'})

                # OTP verified
                otp.is_used = True
                otp.save()

                # Get or create user
                user, created = User.objects.get_or_create(
                    phone_number=phone_number,
                    defaults={'is_active': True}
                )

                # Create WhatsApp profile
                whatsapp_user, _ = WhatsAppUser.objects.get_or_create(
                    phone_number=phone_number,
                    defaults={'user': user, 'is_verified': True}
                )

                # Generate a temporary password for session
                # (We use session-based auth, not password auth)
                user.set_unusable_password()
                user.save()

                # Login user
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                # Clear session
                if 'phone_number' in request.session:
                    del request.session['phone_number']

                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'redirect': 'dashboard:index'
                })

            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        # Regular form submission
        otp_code = request.POST.get('otp_code', '').strip()
        phone_number = request.session.get('phone_number')

        if not phone_number or not otp_code:
            return render(request, 'whatsapp_auth/verify_otp.html', {
                'error': 'Invalid request',
                'phone_number': phone_number
            })

        # Get latest OTP
        otp = OTP.objects.filter(
            phone_number=phone_number,
            is_used=False
        ).order_by('-created_at').first()

        if not otp:
            return render(request, 'whatsapp_auth/verify_otp.html', {
                'error': 'No OTP found. Request a new one.',
                'phone_number': phone_number
            })

        if otp.is_expired():
            return render(request, 'whatsapp_auth/verify_otp.html', {
                'error': 'OTP expired',
                'phone_number': phone_number
            })

        if not otp.is_valid_attempt():
            return render(request, 'whatsapp_auth/verify_otp.html', {
                'error': 'Too many attempts',
                'phone_number': phone_number
            })

        if otp.code != otp_code:
            otp.increment_attempts()
            return render(request, 'whatsapp_auth/verify_otp.html', {
                'error': 'Invalid OTP',
                'phone_number': phone_number
            })

        # OTP verified
        otp.is_used = True
        otp.save()

        # Get or create user
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={'is_active': True}
        )

        # Create WhatsApp profile
        whatsapp_user, _ = WhatsAppUser.objects.get_or_create(
            phone_number=phone_number,
            defaults={'user': user, 'is_verified': True}
        )

        # Login user
        user.set_unusable_password()
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # Clear session
        if 'phone_number' in request.session:
            del request.session['phone_number']

        return redirect('dashboard:index')


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    """Handle user logout."""

    def get(self, request):
        """Logout user."""
        logout(request)
        return redirect('whatsapp_auth:request_otp')
