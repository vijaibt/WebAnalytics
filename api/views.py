from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Event
from .serializers import EventSerializer
from datetime import timedelta
from django.utils import timezone

# Keep the hello_world endpoint for testing
@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello World"})

class EventList(ListCreateAPIView):
    """
    List all events or create a new event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned events by filtering
        against query parameters in the URL.
        """
        queryset = Event.objects.all()
        
        # Filter by event name
        event_name = self.request.query_params.get('event_name', None)
        if event_name:
            queryset = queryset.filter(event_name=event_name)
        
        # Filter by path
        path = self.request.query_params.get('path', None)
        if path:
            queryset = queryset.filter(path=path)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset

class EventDetail(RetrieveAPIView):
    """
    Retrieve a specific event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

@api_view(['GET'])
def event_count_by_day(request):
    """
    Get event counts grouped by day.
    
    Query parameters:
    - event_name: Filter by event type
    - days: Number of days to include (default: 7)
    """
    days = int(request.query_params.get('days', 7))
    event_name = request.query_params.get('event_name', None)
    
    # Calculate the start date
    start_date = timezone.now().date() - timedelta(days=days)
    
    # Base query
    queryset = Event.objects.filter(timestamp__date__gte=start_date)
    
    # Apply event type filter if provided
    if event_name:
        queryset = queryset.filter(event_name=event_name)
    
    # Group by day and count
    daily_counts = (
        queryset
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    
    return Response(daily_counts)

@api_view(['GET'])
def page_views_by_country(request):
    """
    Get page view counts grouped by country.
    """
    days = int(request.query_params.get('days', 30))
    start_date = timezone.now().date() - timedelta(days=days)
    
    country_views = (
        Event.objects.filter(
            event_name='pageview',
            timestamp__date__gte=start_date,
            country__isnull=False
        )
        .values('country')
        .annotate(views=Count('id'))
        .order_by('-views')
    )
    
    return Response(country_views)

@api_view(['GET'])
def top_pages(request):
    """
    Get the most viewed pages.
    """
    days = int(request.query_params.get('days', 30))
    limit = int(request.query_params.get('limit', 10))
    start_date = timezone.now().date() - timedelta(days=days)
    
    top_pages = (
        Event.objects.filter(
            event_name='pageview',
            timestamp__date__gte=start_date
        )
        .values('path', 'title')
        .annotate(views=Count('id'))
        .order_by('-views')[:limit]
    )
    
    return Response(top_pages)

@api_view(['POST'])
def track_event(request):
    """
    Endpoint to receive and store analytics events from the frontend.
    """
    serializer = EventSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)