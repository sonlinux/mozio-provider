# coding: utf-8
from __future__ import absolute_import

__author__ = 'Alison Mukoma <mukomalison@gmail.com'
__date__ = '29/06/19'
__copyright__ = 'mozio.com'


from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.generics import ListAPIView
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView


from provider.models import Provider
from provider.serializers.provider import ProviderSerializer


class ProviderAPIView(ListBulkCreateUpdateDestroyAPIView):
    """
    Allow for:
    Listing,
    Bulk create,
    bulk update,
    bulk delete on provider entries.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def get(self, request, *args):
        providers = self.get_queryset()
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data)
