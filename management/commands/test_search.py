from django.core.management.base import BaseCommand
from search.services import search_houses, analyze_listings

class Command(BaseCommand):
    help = 'Test house search functionality'

    def add_arguments(self, parser):
        parser.add_argument('--location', type=str, default="Nairobi")
        parser.add_argument('--query', type=str, default="family homes")

    def handle(self, *args, **options):
        location = options['location']
        query = options['query']

        self.stdout.write(f"Testing search in {location} for '{query}'...")
        
        try:
            # Test search
            listings = search_houses(location)
            self.stdout.write(f"Found {len(listings)} listings")
            
            # Test analysis
            if listings:
                analysis = analyze_listings(query, listings[:3])
                self.stdout.write("\nAI Analysis:")
                self.stdout.write(analysis)
            
            self.stdout.write(self.style.SUCCESS("Test completed successfully"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Test failed: {str(e)}"))