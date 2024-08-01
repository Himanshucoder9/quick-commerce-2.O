from django.utils import timezone
import datetime
import uuid
from django.conf import settings
from twilio.rest import Client
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from App.settings import TEMPLATES_BASE_URL
from .models import ForgetOTP
from django.core.mail import send_mail
from django.utils.html import strip_tags

twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def new_token():
    token = uuid.uuid1().hex
    return token


def send_otp_customer(user, otp):
    client = twilio_client

    sms_body = render_to_string(
        "auth/customer/customer_register_otp.txt",
        {
            "otp": otp,
            "user": user.name,
        },
    )
    message = client.messages.create(
        body=sms_body, from_=settings.TWILIO_PHONE_NUMBER, to=user.phone
    )


def send_otp_vendor(user, otp):
    client = twilio_client

    sms_body = render_to_string(
        "auth/vendor/vendor_register_otp.txt",
        {
            "otp": otp,
            "user": user.name,
        },
    )
    message = client.messages.create(
        body=sms_body, from_=settings.TWILIO_PHONE_NUMBER, to=user.phone
    )


def send_otp_driver(user, otp):
    client = twilio_client

    sms_body = render_to_string(
        "auth/driver/driver_register_otp.txt",
        {
            "otp": otp,
            "user": user.name,
        },
    )
    message = client.messages.create(
        body=sms_body, from_=settings.TWILIO_PHONE_NUMBER, to=user.phone
    )


def send_delivery_otp_customer(user, otp):
    client = twilio_client

    sms_body = render_to_string(
        "auth/driver/driver_delivery_otp.txt",
        {
            "otp": otp,
            "user": user.name,
        },
    )
    message = client.messages.create(
        body=sms_body, from_=settings.TWILIO_PHONE_NUMBER, to=user.phone
    )


def send_under_review_sms(user):
    client = twilio_client

    sms_body = render_to_string(
        "auth/vendor/under_review.txt",
        {
            "user": user.name,
        },
    )
    message = client.messages.create(
        body=sms_body, from_=settings.TWILIO_PHONE_NUMBER, to=user.phone
    )


def send_approve_vendor_sms(user):
    client = twilio_client

    sms_body = render_to_string(
        "auth/vendor/send_approve_vendor_sms.txt",
        {
            "user": user.name,
            "base_url": TEMPLATES_BASE_URL,
        },
    )
    message = client.messages.create(
        body=sms_body, from_=settings.TWILIO_PHONE_NUMBER, to=user.phone
    )


def send_otp_email_customer(user, otp):
    subject = "Your OTP for registration at Quick Commerce."
    context = {"otp": otp, "user": user.name}

    html_message = render_to_string(
        "auth/customer/customer_register_email_otp.html", context
    )
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(
        subject,
        plain_message,
        email_from,
        recipient_list,
        html_message=html_message,
    )


def send_otp_email_vendor(user, otp):
    subject = "Your OTP for vendor registration at Quick Commerce."
    context = {"otp": otp, "user": user.name}

    html_message = render_to_string("auth/vendor/vendor_register_otp.html", context)
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(
        subject,
        plain_message,
        email_from,
        recipient_list,
        html_message=html_message,
    )


def send_password_reset_sms(user):
    # Initialize Twilio client
    client = twilio_client

    token = new_token()
    exp_time = timezone.now() + datetime.timedelta(minutes=30)
    PasswordResetToken.objects.update_or_create(
        user=user, defaults={"user": user, "token": token, "validity": exp_time}
    )

    # Compose SMS message
    sms_body = render_to_string(
        "auth/password_reset.txt",
        {
            "token": token,
            "phone": user.phone,
            "user": user.name,
            "base_url": TEMPLATES_BASE_URL,
        },
    )

    # Send SMS via Twilio
    try:
        message = client.messages.create(
            body=sms_body, from_=settings.TWILIO_PHONE_NUMBER, to=user.phone
        )
        # print("SMS Sent successfully:", message.sid)
        return Response(
            {"message": "Reset password SMS sent successfully"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        # print("Error sending SMS:", str(e))
        return Response(
            {"message": "Failed to send reset password SMS"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def send_product_restock_email_notification(user, product):
    subject = 'Product Back in Stock!'
    message = f'The product {product.title} is now back in stock. Hurry up!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, email_from, recipient_list)


def send_product_restock_sms_notification(user, product):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'The product {product.title} is now back in stock. Hurry up!',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=user.phone
    )


def send_contact_confirmation_email_to_user(name, email, subject):
    enail_subject = 'Thank you for contacting us!'
    message = f'Hello {name},\n\nThank you for reaching out. We have received your message with the subject "{subject}". Our team will get back to you shortly.\n\nBest regards,\nYour Company Name'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(enail_subject, message, email_from, recipient_list)
