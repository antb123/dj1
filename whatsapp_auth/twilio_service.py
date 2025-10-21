"""
Twilio WhatsApp Service
Handles sending WhatsApp messages via Twilio API
"""
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
import logging
import json

logger = logging.getLogger(__name__)


class TwilioWhatsAppService:
    """Service for sending WhatsApp messages via Twilio."""

    def __init__(self):
        """Initialize Twilio client."""
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.from_number = settings.TWILIO_WHATSAPP_FROM_NUMBER
        self.otp_template_sid = settings.TWILIO_WHATSAPP_RECEIVER_OTP_TEMPLATE_SID
        self.invitation_template_sid = settings.TWILIO_WHATSAPP_RECEIVER_INVITATION_TEMPLATE_SID

        # Validate configuration
        if not self.account_sid or not self.auth_token:
            logger.warning("Twilio credentials not configured")
            self.client = None
        else:
            self.client = Client(self.account_sid, self.auth_token)

    def _format_phone_number(self, phone_number):
        """
        Format phone number for WhatsApp.
        Ensures it has 'whatsapp:' prefix.

        Args:
            phone_number (str): Phone number (e.g., '+13605551234' or '13605551234')

        Returns:
            str: Formatted WhatsApp number (e.g., 'whatsapp:+13605551234')
        """
        phone_number = phone_number.strip()

        # Remove 'whatsapp:' if already present
        if phone_number.startswith('whatsapp:'):
            phone_number = phone_number.replace('whatsapp:', '')

        # Add '+' if not present
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number

        return f'whatsapp:{phone_number}'

    def send_otp(self, phone_number, otp_code):
        """
        Send OTP via WhatsApp.

        Args:
            phone_number (str): Recipient phone number
            otp_code (str): OTP code to send

        Returns:
            dict: Result with 'success' boolean and 'message' or 'error'
        """
        if not self.client:
            logger.error("Twilio client not initialized. Check credentials.")
            return {
                'success': False,
                'error': 'Twilio not configured'
            }

        try:
            to_number = self._format_phone_number(phone_number)

            # Ensure from_number has whatsapp: prefix
            from_number = self.from_number
            if not from_number.startswith('whatsapp:'):
                from_number = f'whatsapp:{from_number}'

            # Try to send using template if template SID is configured
            if self.otp_template_sid:
                message = self._send_template_message(
                    to_number=to_number,
                    from_number=from_number,
                    template_sid=self.otp_template_sid,
                    variables={'otp_code': otp_code}
                )
            else:
                # Fallback to regular message
                message_body = f"Your verification code is: {otp_code}\n\nThis code will expire in 5 minutes."
                message = self.client.messages.create(
                    body=message_body,
                    from_=from_number,
                    to=to_number
                )

            logger.info(f"OTP sent successfully to {phone_number}. Message SID: {message.sid}")

            return {
                'success': True,
                'message': 'OTP sent successfully',
                'message_sid': message.sid
            }

        except TwilioRestException as e:
            logger.error(f"Twilio error sending OTP to {phone_number}: {e.msg} (Code: {e.code})")
            return {
                'success': False,
                'error': f'Failed to send OTP: {e.msg}',
                'error_code': e.code
            }
        except Exception as e:
            logger.error(f"Unexpected error sending OTP to {phone_number}: {str(e)}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }

    def _send_template_message(self, to_number, from_number, template_sid, variables):
        """
        Send a templated WhatsApp message using Twilio Content API.

        Args:
            to_number (str): Recipient number (whatsapp:+...)
            from_number (str): Sender number (whatsapp:+...)
            template_sid (str): Twilio Content Template SID
            variables (dict): Template variables

        Returns:
            Message: Twilio message object
        """
        # Build content variables for template
        content_variables = json.dumps(variables) if variables else None

        message = self.client.messages.create(
            content_sid=template_sid,
            content_variables=content_variables,
            from_=from_number,
            to=to_number
        )

        return message

    def send_invitation(self, phone_number, inviter_name=None):
        """
        Send invitation message via WhatsApp.

        Args:
            phone_number (str): Recipient phone number
            inviter_name (str, optional): Name of person inviting

        Returns:
            dict: Result with 'success' boolean and 'message' or 'error'
        """
        if not self.client:
            logger.error("Twilio client not initialized. Check credentials.")
            return {
                'success': False,
                'error': 'Twilio not configured'
            }

        try:
            to_number = self._format_phone_number(phone_number)

            # Ensure from_number has whatsapp: prefix
            from_number = self.from_number
            if not from_number.startswith('whatsapp:'):
                from_number = f'whatsapp:{from_number}'

            # Try to send using template if template SID is configured
            if self.invitation_template_sid:
                variables = {'inviter_name': inviter_name} if inviter_name else {}
                message = self._send_template_message(
                    to_number=to_number,
                    from_number=from_number,
                    template_sid=self.invitation_template_sid,
                    variables=variables
                )
            else:
                # Fallback to regular message
                invitation_text = "You've been invited to join our lending platform!"
                if inviter_name:
                    invitation_text = f"{inviter_name} has invited you to join our lending platform!"

                invitation_text += "\n\nReply to this message to get started."

                message = self.client.messages.create(
                    body=invitation_text,
                    from_=from_number,
                    to=to_number
                )

            logger.info(f"Invitation sent successfully to {phone_number}. Message SID: {message.sid}")

            return {
                'success': True,
                'message': 'Invitation sent successfully',
                'message_sid': message.sid
            }

        except TwilioRestException as e:
            logger.error(f"Twilio error sending invitation to {phone_number}: {e.msg} (Code: {e.code})")
            return {
                'success': False,
                'error': f'Failed to send invitation: {e.msg}',
                'error_code': e.code
            }
        except Exception as e:
            logger.error(f"Unexpected error sending invitation to {phone_number}: {str(e)}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }


# Singleton instance
_twilio_service = None

def get_twilio_service():
    """Get or create Twilio service instance."""
    global _twilio_service
    if _twilio_service is None:
        _twilio_service = TwilioWhatsAppService()
    return _twilio_service
