from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'timestamp', 'path', 'title', 'country')
    list_filter = ('event_name', 'timestamp', 'country')
    search_fields = ('path', 'title', 'country')
    date_hierarchy = 'timestamp'
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('event_name', 'timestamp', 'received_at')
        }),
        ('Page Information', {
            'fields': ('url', 'path', 'title', 'referrer')
        }),
        ('Marketing Information', {
            'fields': ('utm_source', 'utm_medium', 'utm_campaign'),
            'classes': ('collapse',)
        }),
        ('Geographic Information', {
            'fields': ('country', 'region'),
            'classes': ('collapse',)
        }),
    )