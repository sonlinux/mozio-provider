__author__ = 'Alison Mukoma <mukomalison@gmail>'
__license__ = 'GPL'
__doc__ = ''

from django.db import models
from django.utils.encoding import smart_text
from django.core.urlresolvers import reverse
from django.conf import settings

from .provider import Provider

class Polygon(models.Model):
    """
    Service Area definition.
    """
    name = models.CharField(
        ("Service Area"),
        max_length=255,
        null=True,
        blank=True)

    price = models.CharField(
        ("Price"),
        max_length=255,
        null=True,
        blank=True)

    latitude = models.CharField(
        ("Latitude"),
        max_length=150,
        null=True,
        blank=True)

    longitude = models.CharField(
        ("Longitude"),
        max_length=150,
        null=True,
        blank=True)

    provider = models.ForeignKey(Provider)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service Area'
        verbose_name_plural = 'Service Area'
        app_label = 'provider'

    def __str__(self):
        """smart_text method will allow us to see issues in the admin panel."""
        return smart_text(self.name)

    def __unicode__(self):
        """
        Fail safe option in case we use python version
        not supporting  __str__."""
        return smart_text(self.name)
