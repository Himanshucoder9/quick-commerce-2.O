import re
import uuid
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Regex Validators
def create_regex_validator(pattern, message):
    """Create a RegexValidator with the given pattern and message."""
    return validators.RegexValidator(regex=pattern, message=message)


def mobile_validator(value):
    # Define a regex pattern for the phone number
    pattern = r'^\+?\d{12,12}$'  # Allows optional '+' followed by 10 to 13 digits

    if not re.match(pattern, value):
        raise ValidationError(
            _("Invalid phone number. Ensure it starts with '+91' and contains 10 digits."),
            code='invalid'
        )


# Unique Merchant ID Generator
def generate_merchant_id():
    """Generate a unique merchant ID."""
    return str(uuid.uuid4())


# PAN Validator
def pan_validator(value):
    """Validate PAN card number format."""
    pattern = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]$')
    if not pattern.match(str(value)):
        raise ValidationError(
            _('Enter a valid PAN card number. Example: ABCDE1234F'),
            code='invalid_pan_number'
        )


# GST Validator
def gst_validator(value):
    """Validate GST number format."""
    pattern = re.compile(r'^[0-9A-Za-z]{15}$')
    if not pattern.match(str(value)):
        raise ValidationError(
            _('Enter a valid GST number. It should be 15 alphanumeric characters.'),
            code='invalid_gst_number'
        )


# Length Validators
def minimum(length, msg):
    """Validate minimum length."""
    return validators.MinLengthValidator(length, msg)


def maximum(length, msg):
    """Validate maximum length."""
    return validators.MaxLengthValidator(length, msg)


# Character Type Validators
def alphanumeric(msg):
    """Validate that the input is alphanumeric."""
    return create_regex_validator(
        r'^[a-zA-Z0-9\s]*$',
        f"{msg} must be Alphanumeric!!!"
    )


def alphabet(msg):
    """Validate that the input is alphabetic."""
    return create_regex_validator(
        r'^[a-zA-ZÀ-ÿ\s]*$',
        f"{msg} must be Alphabet!!!"
    )


def numeric(msg):
    """Validate that the input is numeric."""
    return create_regex_validator(
        r'^[0-9]*$',
        f"{msg} must be number!!!"
    )
