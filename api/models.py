from django.db import models

class Event(models.Model):
    """Model to store website visitor events/analytics data."""
    
    EVENT_TYPES = [
        ('pageview', 'Page View'),
        ('click', 'Click'),
        ('form_submit', 'Form Submit'),
        ('scroll_depth', 'Scroll Depth'),
        # Add other event types as needed
    ]
    
    event_name = models.CharField(max_length=50, choices=EVENT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField()
    received_at = models.DateTimeField()
    url = models.URLField(max_length=255)
    path = models.CharField(max_length=255)
    referrer = models.URLField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    
    # UTM parameters
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    
    # Geo information
    country = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_name']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['path']),
            models.Index(fields=['country']),
        ]
    
    def __str__(self):
        return f"{self.event_name} - {self.path} ({self.timestamp})"