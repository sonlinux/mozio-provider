# coding: utf-8
from __future__ import absolute_import

__author__ = 'Alison Mukoma <mukomalison@gmail.com'
__date__ = '29/06/19'
__copyright__ = 'mozio.com'


from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.generics import ListAPIView
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView


from provider.models import Polygon
from ..serializers.service_area import PolygonSerializer


class ServiceAreaAPIView(ListBulkCreateUpdateDestroyAPIView):
    """
    Allow for:
    Listing,
    Bulk create,
    bulk update,
    bulk delete on service area entries.
    """
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer

    def get(self, request, *args):
        service_areas = self.get_queryset()
        serializer = PolygonSerializer(service_areas, many=True)
        return Response(serializer.data)
