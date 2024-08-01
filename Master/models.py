from django.db import models


# Create your models here.

class TimeStamp(models.Model):
    created_at = models.DateTimeField(verbose_name="created date", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated date", auto_now=True)

    class Meta:
        verbose_name = 'TimeStamp'
        verbose_name_plural = 'TimeStamps'
        abstract = True


class SEO(models.Model):
    meta_title = models.CharField(verbose_name='meta title', max_length=200, blank=True, null=True)
    meta_keyword = models.TextField(verbose_name='meta keywords', blank=True, null=True)
    meta_description = models.TextField(verbose_name='meta description', blank=True, null=True)
    canonical = models.URLField(verbose_name='canonical link', blank=True, null=True)

    class Meta:
        verbose_name = 'SEO'
        verbose_name_plural = 'SEO'
        abstract = True


class Address(models.Model):
    building_name = models.CharField(verbose_name="building name", max_length=100, blank=True, null=True)
    street_name = models.CharField(verbose_name="street name", max_length=100, blank=True, null=True)
    zip = models.CharField(verbose_name="zip code", max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name="city", max_length=200, blank=True, null=True)
    state = models.CharField(verbose_name="state", max_length=250, blank=True, null=True)
    latitude = models.DecimalField(verbose_name="Latitude", max_digits=9, decimal_places=6)
    longitude = models.DecimalField(verbose_name="Longitude", max_digits=9, decimal_places=6)
    full_address = models.TextField(verbose_name="full address", blank=True, null=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        abstract = True
