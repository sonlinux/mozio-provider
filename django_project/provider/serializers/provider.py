# coding: utf-8
from __future__ import absolute_import

__author__ = 'Alison Mukoma <mukomalison@gmail.com'
__date__ = '02/05/19'
__copyright__ = 'mozio.com'

from rest_framework import serializers
from rest_framework_bulk import (
    BulkSerializerMixin,
    BulkListSerializer)

from ..models.provider import Provider

class ProviderSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    Serializer object for Provider model.
    """

    class Meta:
        model = Provider
        provider_serializer_class = BulkListSerializer
        fields = '__all__'
