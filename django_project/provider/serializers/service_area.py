# coding: utf-8
from __future__ import absolute_import
__author__ = 'Alison Mukoma <mukomalison@gmail.com'
__date__ = '03/05/19'
__copyright__ = 'mozio.com'


from rest_framework import serializers
from rest_framework_bulk import (
    BulkSerializerMixin,
    BulkListSerializer)

from provider.models.service_area import Polygon

class PolygonSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    Serializer object for Polygon model.
    """

    class Meta:
        model = Polygon
        list_serializer_class = BulkListSerializer
        fields = '__all__'
