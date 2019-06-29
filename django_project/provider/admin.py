from django.contrib import admin

from provider.models.provider import Provider
from provider.models.service_area import Polygon

class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'Currency']
    readonly_fields = ['created', 'updated']
    fieldsets = (
        ('Main details', {
            'fields': ('name', 'email', )
        }),
        ('Other properties', {
            'classes': ('collapse',),
            'fields': ('phone_number', 'Currency', 'updated'),
        }),
    )

class PolygonAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'latitude', 'longitude']
    readonly_fields = ['created', 'updated']
    fieldsets = (
        ('Main details', {
            'fields': ('name', 'price', )
        }),
        ('Other properties', {
            'classes': ('collapse',),
            'fields': ('latitude', 'longitude' 'updated'),
        }),
    )
admin.site.register(Provider, ProviderAdmin)
