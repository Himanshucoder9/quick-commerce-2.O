from django.utils import timezone
import datetime
import uuid
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from App.settings import TEMPLATES_BASE_URL
from Auth.models import ForgetOTP
from django.core.mail import send_mail
from django.utils.html import strip_tags


def send_customer_register_email_otp(user, otp):
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


def send_warehouse_register_email_otp(user, otp):
    subject = "Your OTP for registration at Quick Commerce."
    context = {"otp": otp, "user": user.name}

    html_message = render_to_string(
        "auth/warehouse/warehouse_register_email_otp.html", context
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
