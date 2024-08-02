from django.db import models
from imagekit.models import ProcessedImageField
from Master.models import TimeStamp, SEO
from Master.myvalidator import mobile_validator
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _


class Country(TimeStamp):
    name = models.CharField(max_length=100, verbose_name=_("country"))
    code = models.CharField(max_length=10, verbose_name=_("country code"))

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return f"{self.code} - {self.name}"


class State(TimeStamp):
    name = models.CharField(max_length=200, verbose_name=_("state name"))
    code = models.CharField(max_length=200, verbose_name=_("state code"))
    is_available = models.BooleanField(default=True, verbose_name=_("is available"))

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")

    def __str__(self):
        return self.name


class City(TimeStamp):
    name = models.CharField(max_length=200, verbose_name=_("city name"))
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name=_("state"), related_name="cities")
    is_available = models.BooleanField(default=True, verbose_name=_("is available"))

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return self.name


class SiteConfig(SEO, TimeStamp):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    favicon = models.ImageField(upload_to="core/siteconfig/favicon/", verbose_name=_("favicon"))
    logo = ProcessedImageField(
        upload_to="core/siteconfig/logo/",
        format="WEBP",
        options={"quality": 50},
        verbose_name=_("logo"),
    )
    primary_mobile = models.CharField(
        max_length=13,
        validators=[mobile_validator],
        verbose_name=_("primary mobile number"),
        help_text=_("Alphabets and special characters are not allowed."),
    )
    secondary_mobile = models.CharField(
        max_length=13,
        validators=[mobile_validator],
        verbose_name=_("secondary mobile number"),
        help_text=_("Alphabets and special characters are not allowed."),
        blank=True,
        null=True,
    )
    email = models.EmailField(max_length=255, verbose_name=_("email"))
    short_description = models.TextField(verbose_name=_("short description"), blank=True, null=True)
    address = models.TextField(verbose_name=_("address"), blank=True, null=True)
    playstore = models.URLField(verbose_name=_("playstore app url"), blank=True, null=True)
    appstore = models.URLField(verbose_name=_("appstore app url"), blank=True, null=True)

    class Meta:
        verbose_name = _("Site Config")
        verbose_name_plural = _("Site Config")

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

    site_config = models.ForeignKey(SiteConfig, on_delete=models.CASCADE, related_name="social_media")
    name = models.CharField(max_length=20, choices=SOCIAL_CHOICES, unique=True, verbose_name=_("platform"))
    url = models.URLField(verbose_name=_("URL"))

    class Meta:
        verbose_name = _("Social Media")
        verbose_name_plural = _("Social Media")

    def __str__(self):
        return self.name


class About(SEO, TimeStamp):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    description = CKEditor5Field(verbose_name=_("description"), config_name="extends")

    class Meta:
        verbose_name = _("About Us")
        verbose_name_plural = _("About Us")

    def __str__(self):
        return self.title


class PrivacyPolicy(SEO, TimeStamp):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    description = CKEditor5Field(verbose_name=_("description"), config_name="extends")

    class Meta:
        verbose_name = _("Privacy Policy")
        verbose_name_plural = _("Privacy Policies")

    def __str__(self):
        return self.title


class TermsAndCondition(SEO, TimeStamp):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    description = CKEditor5Field(verbose_name=_("description"), config_name="extends")

    class Meta:
        verbose_name = _("Terms & Conditions")
        verbose_name_plural = _("Terms & Conditions")

    def __str__(self):
        return self.title


class FAQCategory(SEO, TimeStamp):
    title = models.CharField(max_length=50, unique=True, verbose_name=_("category title"))

    class Meta:
        verbose_name = _("FAQ Category")
        verbose_name_plural = _("FAQ Categories")

    def __str__(self):
        return self.title


class FAQ(SEO, TimeStamp):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, blank=True, null=True, related_name="faqs")
    question = models.CharField(max_length=250, verbose_name=_("question"))
    answer = CKEditor5Field(verbose_name=_("answer"), config_name="extends")

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")

    def __str__(self):
        return self.question


class Contact(TimeStamp):
    name = models.CharField(max_length=200, verbose_name=_("full name"))
    email = models.EmailField(max_length=255, verbose_name=_("email address"))
    mobile = models.CharField(max_length=15, verbose_name=_("mobile number"))
    subject = models.CharField(max_length=200, verbose_name=_("subject"))
    message = models.TextField(verbose_name=_("message"))

    class Meta:
        verbose_name = _("Contact Us")
        verbose_name_plural = _("Contact Us")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} - {self.email} - {self.subject}"


class Feedback(TimeStamp):
    name = models.CharField(max_length=200, verbose_name=_("full name"))
    message = models.TextField(blank=True, null=True, verbose_name=_("message"))
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_("rating"))

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedback")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} - {self.rating}"
