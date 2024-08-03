import random
import string
from django.utils import timezone
from datetime import timedelta

from Auth.models import ForgetOTP, OTP


def generate_otp():
    otp = random.randint(100000, 999999)
    return otp


def send_otp_to_phone(email, otp):
    # Implement the logic to send OTP to the user's phone
    # For example, using an SMS gateway API
    pass


def verify_otp(user, otp):
    try:
        otp_record = ForgetOTP.objects.get(user=user)
    except ForgetOTP.DoesNotExist:
        return False

    # Check if OTP is expired
    if timezone.now() > otp_record.created_at + timedelta(minutes=15):
        otp_record.delete()  # Optionally clean up expired OTP records
        return False

    # Check if OTP matches
    if otp_record.otp == otp:
        otp_record.delete()  # Optionally clean up after successful verification
        return True

    return False


def verify_profile_delete_otp(user, otp):
    try:
        otp_record = OTP.objects.get(user=user)
    except OTP.DoesNotExist:
        return False

    # Check if OTP is expired
    if timezone.now() > otp_record.created_at + timedelta(minutes=15):
        otp_record.delete()  # Optionally clean up expired OTP records
        return False

    # Check if OTP matches
    if otp_record.otp == otp:
        otp_record.delete()  # Optionally clean up after successful verification
        return True

    return False



