from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import SearchQuery, HouseListing
from .services import search_houses, process_search_results, analyze_listings
from urllib.parse import quote_plus
from groq import Groq
import os

import markdown


def home(request):
    """Render the home page search form"""
    return render(request, 'nyumbaAI_app/index.html')

def search(request):
    """Handle property search requests"""
    if request.method == 'POST':
        try:
            # Get form data
            raw_query = request.POST.get('query', '')
            location = request.POST.get('location', '')

            # Validate required fields
            if not location:
                return HttpResponseBadRequest("Location is required")

            # Perform house search
            raw_results = search_houses(location)
            processed_listings = process_search_results(raw_results)

            # Save search to database
            search_query = SearchQuery.objects.create(
                query=raw_query,
                location=location,
                results_count=len(processed_listings)
            )

            # Save listings with fallback values
            for listing in processed_listings:
                HouseListing.objects.create(
                    search=search_query,
                    title=listing.get('title', 'No Title Available'),
                    price=listing.get('price', 'Price Not Available'),
                    address=listing.get('address', 'Address Not Available'),
                    link=listing.get('link', '#'),
                    latitude=listing.get('latitude'),
                    longitude=listing.get('longitude'),
                    rating=listing.get('rating'),
                    description=listing.get('description', 'No Description Available')
                )

            # Generate analysis
            analysis = analyze_listings(raw_query, processed_listings)
            analysis_html = markdown.markdown(analysis)
            

            # Create Google Maps URL
            encoded_location = quote_plus(location)
            maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_location}"

            context = {
                'listings': processed_listings,
                "analysis": analysis_html,

                'analysis': analysis,

                'query': raw_query,
                'location': location,
                'maps_url': maps_url,
                'raw_results': raw_results if os.getenv('DEBUG') else None
            }

            return render(request, 'nyumbaAI_app/results.html', context)

        except Exception as e:
            # Log error and show error page
            print(f"Search error: {str(e)}")
            return render(request, 'nyumbaAI_app/error.html', {
                'error_message': "Could not complete search. Please try again."
            })

    return redirect('nyumbaAI_app:home')