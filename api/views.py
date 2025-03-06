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

# Add these to your api/views.py file

@api_view(['GET'])
def traffic_sources(request):
    """
    Get traffic sources data grouped by UTM source.
    """
    days = int(request.query_params.get('days', 7))
    start_date = timezone.now().date() - timedelta(days=days)
    
    # Group by source and calculate metrics
    sources = (
        Event.objects.filter(timestamp__date__gte=start_date)
        .values('utm_source')
        .annotate(
            sessions=Count('session_id', distinct=True),
            bounces=Count(Case(
                When(session_id__in=Subquery(
                    Event.objects.filter(
                        timestamp__date__gte=start_date
                    ).values('session_id').annotate(
                        count=Count('id')
                    ).filter(count=1).values('session_id')
                ), then=1),
                output_field=IntegerField()
            ))
        )
        .annotate(
            bounce_rate=ExpressionWrapper(
                F('bounces') * 100.0 / F('sessions'),
                output_field=FloatField()
            )
        )
        .order_by('-sessions')
    )
    
    # Format the results
    result = []
    for source in sources:
        result.append({
            'source': source['utm_source'] or '(not set)',
            'sessions': source['sessions'],
            'bounces': source['bounces'],
            'bounceRate': source['bounce_rate']
        })
    
    # Add overall stats
    total_sessions = sum(item['sessions'] for item in result)
    total_bounces = sum(item['bounces'] for item in result)
    
    if total_sessions > 0:
        overall_bounce_rate = (total_bounces * 100.0) / total_sessions
    else:
        overall_bounce_rate = 0
    
    result.append({
        'source': 'Overall',
        'sessions': total_sessions,
        'bounces': total_bounces,
        'bounceRate': overall_bounce_rate
    })
    
    return Response(result)

@api_view(['GET'])
def page_metrics(request):
    """
    Get page view metrics and trends.
    """
    days = int(request.query_params.get('days', 7))
    start_date = timezone.now().date() - timedelta(days=days)
    
    # Get total page views
    total_views = Event.objects.filter(
        timestamp__date__gte=start_date,
        event_name='pageview'
    ).count()
    
    # Get total unique users
    unique_users = Event.objects.filter(
        timestamp__date__gte=start_date
    ).values('user_id').distinct().count()
    
    # Calculate average pages per user
    avg_per_user = 0
    if unique_users > 0:
        avg_per_user = total_views / unique_users
    
    # Get trend data
    trend = (
        Event.objects.filter(
            timestamp__date__gte=start_date,
            event_name='pageview'
        )
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(
            views=Count('id'),
            users=Count('user_id', distinct=True)
        )
        .order_by('date')
    )
    
    # Calculate average pages per user for each day
    trend_data = []
    for day in trend:
        avg_pages = 0
        if day['users'] > 0:
            avg_pages = day['views'] / day['users']
        
        trend_data.append({
            'date': day['date'],
            'avg_pages_per_user': avg_pages
        })
    
    result = {
        'total_views': total_views,
        'avg_per_user': avg_per_user,
        'trend': trend_data
    }
    
    return Response(result)

@api_view(['GET'])
def top_pages(request):
    """
    Get performance metrics for top pages.
    """
    days = int(request.query_params.get('days', 7))
    limit = int(request.query_params.get('limit', 10))
    start_date = timezone.now().date() - timedelta(days=days)
    
    # Get page views
    page_views = (
        Event.objects.filter(
            timestamp__date__gte=start_date,
            event_name='pageview'
        )
        .values('path', 'title')
        .annotate(views=Count('id'))
        .order_by('-views')[:limit]
    )
    
    # Get landing pages (first touch)
    landing_pages = (
        Event.objects.filter(
            timestamp__date__gte=start_date
        )
        .values('path')
        .annotate(count=Count('session_id', distinct=True))
        .order_by('-count')
    )
    
    # Get exit pages (last touch)
    exit_pages = (
        Event.objects.filter(
            timestamp__date__gte=start_date
        )
        .values('path', 'session_id')
        .annotate(last_touch=Max('timestamp'))
        .values('path')
        .annotate(count=Count('session_id'))
        .order_by('-count')
    )
    
    # Calculate bounce rates
    bounce_rates = {}
    for path in set([p['path'] for p in page_views]):
        sessions = Event.objects.filter(
            timestamp__date__gte=start_date,
            path=path
        ).values('session_id').distinct().count()
        
        bounces = Event.objects.filter(
            timestamp__date__gte=start_date,
            path=path,
            session_id__in=Subquery(
                Event.objects.filter(
                    timestamp__date__gte=start_date
                ).values('session_id').annotate(
                    count=Count('id')
                ).filter(count=1).values('session_id')
            )
        ).values('session_id').distinct().count()
        
        if sessions > 0:
            bounce_rates[path] = (bounces * 100.0) / sessions
        else:
            bounce_rates[path] = 0
    
    # Combine the data
    result = []
    for page in page_views:
        path = page['path']
        landing_count = next((p['count'] for p in landing_pages if p['path'] == path), 0)
        exit_count = next((p['count'] for p in exit_pages if p['path'] == path), 0)
        
        result.append({
            'page': page['title'] or path,
            'views': page['views'],
            'landing_page': landing_count,
            'exit_page': exit_count,
            'bounce_rate': bounce_rates.get(path, 0)
        })
    
    return Response(result)

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