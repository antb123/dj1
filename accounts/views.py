from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import View
from .forms import UserRegistrationForm, UserLoginForm, CustomPasswordResetForm
from .tokens import email_verification_token
from .models import User


class RegisterView(View):
    """Handle user registration."""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # User can login but email not verified
            user.save()

            # Send verification email
            self.send_verification_email(request, user)

            messages.success(request, 'Registration successful! Please check your email to verify your account.')
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {'form': form})

    def send_verification_email(self, request, user):
        """Send email verification link to user."""
        token = email_verification_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = request.build_absolute_uri(
            f'/accounts/verify-email/{uid}/{token}/'
        )

        subject = 'Verify your email address'
        message = render_to_string('accounts/email_verification.html', {
            'user': user,
            'verification_link': verification_link,
        })

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


class VerifyEmailView(View):
    """Handle email verification."""

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and email_verification_token.check_token(user, token):
            user.is_email_verified = True
            user.save()
            messages.success(request, 'Email verified successfully! You can now login.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid verification link.')
            return redirect('accounts:login')


class CustomLoginView(LoginView):
    """Handle user login."""

    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Override to check email verification."""
        user = form.get_user()
        if not user.is_email_verified:
            messages.warning(self.request, 'Please verify your email address before logging in.')
            return redirect('accounts:login')
        return super().form_valid(form)


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


class CustomPasswordResetView(PasswordResetView):
    """Handle password reset request."""

    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        messages.success(self.request, 'Password reset email sent! Please check your inbox.')
        return super().form_valid(form)
