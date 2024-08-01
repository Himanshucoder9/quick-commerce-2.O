from django.db import models
from imagekit.models import ProcessedImageField
from Master.models import *
from Master.myvalidator import mobile_validator
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class SiteConfig(SEO, TimeStamp):
    title = models.CharField(verbose_name='title', max_length=100)
    favicon = models.ImageField(verbose_name='favicon', upload_to='core/siteconfig/favicon/')
    logo = ProcessedImageField(
        upload_to='core/siteconfig/logo/',
        format='WEBP',
        options={'quality': 50}, verbose_name="logo"
    )
    primary_mobile = models.CharField(verbose_name="primary mobile number", max_length=13,
                                      validators=[mobile_validator],
                                      help_text="Alphabets and special characters are not allowed.")
    secondary_mobile = models.CharField(verbose_name="secondary mobile number", max_length=13,
                                        validators=[mobile_validator],
                                        help_text="Alphabets and special characters are not allowed.", blank=True,
                                        null=True)
    email = models.EmailField(verbose_name='email', max_length=255)
    short_description = models.TextField(verbose_name='short description', blank=True, null=True)
    address = models.TextField(verbose_name='address', blank=True, null=True)

    class Meta:
        verbose_name = 'Site Config'
        verbose_name_plural = 'Site Config'

    def __str__(self):
        return self.title


class SocialMedia(TimeStamp):
    SOCIAL_CHOICES = (
        ("whatsapp", "Whatsapp"),
        ("linkedin", "Linkedin"),
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("threads", "Threads"),
        ("x", "X"),
        ("youtube", "Youtube"),
        ("playstore", "Playstore"),
        ("appstore", "Appstore"),
    )
    site_config = models.ForeignKey(SiteConfig, on_delete=models.CASCADE)
    name = models.CharField(choices=SOCIAL_CHOICES, verbose_name="platform", max_length=20, unique=True)
    url = models.URLField(verbose_name="URL")

    class Meta:
        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'

    def __str__(self):
        return self.name


# class Banner(TimeStamp):
#     image = ProcessedImageField(
#         upload_to='core/banner/',
#         format='WEBP',
#         options={'quality': 50}, verbose_name="banner image"
#     )

#     class Meta:
#         verbose_name = 'Banner'
#         verbose_name_plural = 'Banners'


class About(SEO, TimeStamp):
    title = models.CharField(verbose_name='title', max_length=100)
    description = CKEditor5Field(verbose_name='description', config_name='extends')

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def __str__(self):
        return self.title


class PrivacyPolicy(SEO, TimeStamp):
    title = models.CharField(verbose_name='title', max_length=200)
    description = CKEditor5Field(verbose_name='description', config_name='extends')

    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policy'

    def __str__(self):
        return self.title


class TermsAndCondition(SEO, TimeStamp):
    title = models.CharField(verbose_name='title', max_length=200)
    description = CKEditor5Field(verbose_name='description', config_name='extends')

    class Meta:
        verbose_name = 'Terms & Condition'
        verbose_name_plural = 'Terms & Condition'

    def __str__(self):
        return self.title


class FAQCategory(SEO, TimeStamp):
    title = models.CharField(verbose_name='category title', max_length=50, unique=True)

    class Meta:
        verbose_name = 'FAQ Category'
        verbose_name_plural = 'FAQ Categories'

    def __str__(self):
        return self.title


class FAQ(SEO, TimeStamp):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, blank=True, null=True)
    question = models.CharField(verbose_name='question', max_length=250)
    answer = CKEditor5Field(verbose_name='answer', config_name='extends')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class Contact(TimeStamp):
    name = models.CharField(max_length=200, verbose_name='full name')
    email = models.EmailField(max_length=255, verbose_name='email address')
    mobile = models.CharField(max_length=15, verbose_name='mobile number')
    subject = models.CharField(max_length=200, verbose_name='subject')
    message = models.TextField(verbose_name='message')

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.email} {self.subject}"


class Feedback(TimeStamp):
    name = models.CharField(max_length=200, verbose_name='full name')
    message = models.TextField(verbose_name='message')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.message} {self.rating}"


class Country(TimeStamp):
    code = models.CharField(max_length=10, verbose_name="country code")
    name = models.CharField(max_length=100, verbose_name="country")

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return f"{self.code} - {self.name}"
    

class State(TimeStamp):
    name = models.CharField(max_length=200, verbose_name='state name')
    abbreviation = models.CharField(max_length=200, verbose_name='abbreviation')
    is_available = models.BooleanField(default=True, verbose_name="is available")

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return self.name


class City(TimeStamp):
    name = models.CharField(max_length=200, verbose_name='city name')
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='state')
    is_available = models.BooleanField(default=True, verbose_name="is available")

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name



