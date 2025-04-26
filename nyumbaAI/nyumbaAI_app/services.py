from groq import Groq
from serpapi import GoogleSearch
import os
from typing import List, Dict, Any

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def search_houses(location: str) -> dict:
    """Fetch raw API response and normalize structure"""
    try:
        if not location or not isinstance(location, str):
            return {"local_results": []}

        params = {
            "engine": "google_local",
            "q": "houses for sale",
            "location": location,
            "api_key": os.getenv('SERP_API_KEY'),
            "hl": "en",
            "gl": "us"
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        # Normalize response structure
        if isinstance(results, list):
            return {"local_results": results}
        if "local_results" not in results:
            return {"local_results": []}
            
        return results

    except Exception as e:
        print(f"Search error: {str(e)}")
        return {"local_results": []}

def process_search_results(raw_results: dict) -> List[Dict[str, Any]]:
    """Convert normalized API response to structured listings"""
    processed = []
    listings = raw_results.get("local_results", [])
    
    # Handle different result formats
    if isinstance(listings, dict):
        listings = [listings]
    elif not isinstance(listings, list):
        return []

    for item in listings:
        processed.append({
            "title": item.get("title", "No Title Available"),
            "price": item.get("price", "Price Not Available"),
            "address": item.get("address", "Address Not Available"),
            "latitude": item.get("gps_coordinates", {}).get("latitude"),
            "longitude": item.get("gps_coordinates", {}).get("longitude"),
            "rating": item.get("rating"),
            "description": item.get("description", "No Description Available"),
            "link": item.get("link") or  # Try direct link first
            item.get("links", {}).get("website") or  # Alternative key
            item.get("directions", {}).get("google_url") or  # Fallback to maps
            "#"  # Ultimate fallback
        })
    
    return processed

def analyze_listings(query: str, listings: List[Dict]) -> str:
    """Generate analysis using Groq API"""
    try:
        if not listings:
            return "No listings available for analysis"

        listings_text = "\n".join(
            [f"{l.get('title', 'Unknown')} - {l.get('price', 'N/A')} ({l.get('address', 'Unknown location')})" 
             for l in listings]
        )
        
        prompt = f"""Real Estate Analysis Request: {query}

        Listings to Analyze:
        {listings_text}

        Provide detailed analysis covering:
        - Price trends and comparisons
        - Location advantages/disadvantages
        - Property value assessment
        - Potential concerns to consider
        - Purchase recommendations

        Format using markdown with clear sections."""

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=os.getenv('GROQ_MODEL_NAME', 'mistral-saba-24b'),
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return "Could not generate analysis"