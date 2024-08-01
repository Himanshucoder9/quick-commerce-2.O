from django.db import models
from django.utils.translation import gettext_lazy as _


# Abstract model for timestamps
class TimeStamp(models.Model):
    created_at = models.DateTimeField(verbose_name=_("created date"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("TimeStamp")
        verbose_name_plural = _("TimeStamps")
        abstract = True


# Abstract model for SEO fields
class SEO(models.Model):
    meta_title = models.CharField(verbose_name=_("meta title"), max_length=200, blank=True, null=True)
    meta_keyword = models.TextField(verbose_name=_("meta keywords"), blank=True, null=True)
    meta_description = models.TextField(verbose_name=_("meta description"), blank=True, null=True)
    canonical = models.URLField(verbose_name=_("canonical link"), blank=True, null=True)

    class Meta:
        verbose_name = _("SEO")
        verbose_name_plural = _("SEO")
        abstract = True


# Abstract model for Address fields
class Address(models.Model):
    building_name = models.CharField(verbose_name=_("building name"), max_length=100, blank=True, null=True)
    street_name = models.CharField(verbose_name=_("street name"), max_length=100, blank=True, null=True)
    zip = models.CharField(verbose_name=_("zip code"), max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name=_("city"), max_length=200, blank=True, null=True)
    state = models.CharField(verbose_name=_("state"), max_length=250, blank=True, null=True)
    latitude = models.DecimalField(verbose_name=_("latitude"), max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(verbose_name=_("longitude"), max_digits=9, decimal_places=6, blank=True, null=True)
    full_address = models.TextField(verbose_name=_("full address"), blank=True, null=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        abstract = True
