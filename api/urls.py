from django.urls import path
from . import views

urlpatterns = [
    # Keep the hello_world endpoint for testing
    path('hello/', views.hello_world, name='hello_world'),
    
    # Event endpoints
    path('events/', views.EventList.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
    
    # Analytics endpoints
    path('analytics/daily/', views.event_count_by_day, name='daily-events'),
    path('analytics/countries/', views.page_views_by_country, name='country-views'),
    path('analytics/top-pages/', views.top_pages, name='top-pages'),
    
    # Tracking endpoint
    path('track/', views.track_event, name='track-event'),
]