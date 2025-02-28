import os
import csv
import datetime
from django.core.management.base import BaseCommand
from api.models import Event

class Command(BaseCommand):
    help = 'Import sample events data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f"File {csv_file} does not exist"))
            return
        
        self.stdout.write(f"Importing data from {csv_file}...")
        
        # Create directory structure if it doesn't exist
        os.makedirs('api/management/commands', exist_ok=True)
        
        events_created = 0
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # Parse timestamps
                    timestamp = datetime.datetime.strptime(
                        row.get('timestamp', ''), 
                        '%Y-%m-%d %H:%M:%S'
                    )
                    
                    received_at = datetime.datetime.strptime(
                        row.get('received_at', ''), 
                        '%Y-%m-%d %H:%M:%S'
                    )
                    
                    # Create Event object
                    Event.objects.create(
                        event_name=row.get('event_name', ''),
                        timestamp=timestamp,
                        received_at=received_at,
                        url=row.get('url', ''),
                        path=row.get('path', ''),
                        referrer=row.get('referrer', None) or None,  # Convert empty strings to None
                        title=row.get('title', None) or None,
                        utm_source=row.get('utm_source', None) or None,
                        utm_medium=row.get('utm_medium', None) or None,
                        utm_campaign=row.get('utm_campaign', None) or None,
                        country=row.get('country', None) or None,
                        region=row.get('region', None) or None,
                    )
                    
                    events_created += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Error importing row: {row}\nError: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f"Successfully imported {events_created} events"))