__author__ = 'Alison Mukoma <mukomalison@gmail>'
__doc__ = ''

from django.db import models
from django.utils.encoding import smart_text
from django.core.urlresolvers import reverse
from django.conf import settings


class Provider(models.Model):
    """
    Provider model definition.
    """
    name = models.CharField(
        ("Provider Name"),
        max_length=255,
        null=True,
        blank=True)

    email = models.EmailField(("Email"))

    phone_number = models.CharField(
        ("Phone Number"),
        max_length=150,
        null=True,
        blank=True)

    language = models.CharField(
        ("Language"),
        max_length=150,
        null=True,
        blank=True)

    Currency = models.CharField(
        ("Currency"),
        max_length=150,
        null=True,
        blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Provider Entry'
        verbose_name_plural = 'Provider Entries'
        app_label = 'provider'

    def __str__(self):
        """smart_text method will allow us to see issues in the admin panel."""
        return smart_text(self.name)

    def __unicode__(self):
        """
        Fail safe option in case we use python version
        not supporting  __str__."""
        return smart_text(self.name)
