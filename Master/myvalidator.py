from django.core import validators
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid


phone_regex = RegexValidator(
    regex=r"^989\d{2}\s*?\d{3}\s*?\d{4}$", message="Invalid phone number.",
)
mobile_validator = RegexValidator(
        regex=r'^\+\d{1,13}$',
        message='Mobile number must be in the format "+911234567890".',
        code='invalid_mobile_format'
    )


def generate_merchant_id():
    return str(uuid.uuid4())


def pan_validator(value):
    pattern = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]$')
    if not pattern.match(str(value)):
        raise ValidationError(
            _('Enter a valid PAN card number. Example: ABCDE1234F'),
            code='invalid_pan_number'
        )
    
def gst_validator(value):
    pattern = re.compile(r'^[0-9A-Za-z]{15}$')
    if not pattern.match(str(value)):
        raise ValidationError(
            _('Enter a valid GST number. It should be 15 alphanumeric characters.'),
            code='invalid_gst_number'
        )
    

def alphanumeric(msg):
    alpha = validators.RegexValidator(r'^[a-zA-Z0-9\s]*$', message=f"{msg} must be Alphanumeric!!!")
    return alpha


def minimum(length, msg):
    minlen = validators.MinLengthValidator(
        length, msg)
    return minlen


def maximum(length, msg):
    maxlen = validators.MaxLengthValidator(
        length, msg)
    return maxlen


def alphabet(msg):
    aerror = validators.RegexValidator(r'^[a-zA-ZÀ-ÿ\s]*$', message=f"{msg} must be Alphabet!!!")
    return aerror


def numeric(msg):
    nerror = validators.RegexValidator(
        r'^[0-9]*$', message=f"{msg} must be number!!!")
    return nerror
