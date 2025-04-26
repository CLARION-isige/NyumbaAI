from typing import List, Dict, Any, Optional
import os
from serpapi import GoogleSearch
from groq import Groq
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PropertySearchEngine:
    def __init__(self):
        self.serp_api_key = os.getenv('SERP_API_KEY')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.groq_client = Groq(api_key=self.groq_api_key) if self.groq_api_key else None
        
    def validate_inputs(self, location: str) -> None:
        """Validate input parameters"""
        if not location or not isinstance(location, str):
            raise ValueError("Location must be a non-empty string")
        if not self.serp_api_key:
            raise ValueError("SERP_API_KEY environment variable not set")
        if not self.groq_client:
            raise ValueError("GROQ_API_KEY environment variable not set")

    def search_properties(self, location: str) -> List[Dict[str, Any]]:
        """Search for properties using SerpAPI"""
        try:
            params = {
                "engine": "google_local",
                "q": "Houses for sale",
                "location": location,
                "api_key": self.serp_api_key
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            return results.get("local_results", [])
            
        except Exception as e:
            logger.error(f"Property search failed: {str(e)}")
            return []

    def process_property_data(self, raw_properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process raw property data into structured format"""
        processed_properties = []
        
        for prop in raw_properties:
            # Extract price if available in description
            price = "Price not specified"
            description = prop.get("description", "")
            if description and "KSh" in description:
                # Simple extraction, can be enhanced
                price = description.split("KSh")[1].strip() if "KSh" in description else "Price not specified"
            
            processed_prop = {
                "name": prop.get("title", "Unknown Property"),
                "type": prop.get("type", "Property"),
                "rating": float(prop.get("rating", 0)),
                "reviews": int(prop.get("reviews", 0)),
                "address": prop.get("address", "Address not available"),
                "contact": prop.get("phone", "Contact not available"),
                "hours": prop.get("hours", "Hours not specified"),
                "years_in_business": prop.get("years_in_business", ""),
                "map_link": prop.get("links", {}).get("directions", ""),
                "website": prop.get("links", {}).get("website", ""),
                "coordinates": prop.get("gps_coordinates", {}),
                "description": description,
                "price": price
            }
            processed_properties.append(processed_prop)
            
        return processed_properties

    def generate_recommendations(self, properties: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        """Generate property recommendations based on multiple factors"""
        if not properties:
            return []
        
        # Score properties based on rating, reviews, and business longevity
        for prop in properties:
            rating_score = prop["rating"] * 2  # Weight rating more
            reviews_score = min(prop["reviews"] * 0.1, 5)  # Cap reviews influence
            longevity_score = 1 if prop.get("years_in_business") else 0
            
            prop["recommendation_score"] = rating_score + reviews_score + longevity_score
        
        # Sort by recommendation score
        sorted_properties = sorted(properties, key=lambda x: x["recommendation_score"], reverse=True)
        
        return sorted_properties[:top_n]

    def create_llm_response(self, properties: List[Dict[str, Any]], user_query: Optional[str] = None) -> str:
        """Generate natural language response using Groq"""
        try:
            prompt = f"""
            The user asked: "{user_query if user_query else 'Show properties'}"
            
            Here are the property listings in Kenya:
            {properties}
            
            Please present the properties in a helpful, conversational manner including:
            - Property name and type
            - Location/address
            - Contact information
            - Opening hours/availability
            - Rating and number of reviews
            - Price information (if available)
            - Map directions link (if available)
            
            Then make 2-3 recommendations at the end based on:
            1. Highest rated properties
            2. Most reviewed properties
            3. Established businesses with years in business
            4. Best value based on features and price (if price is available)
            
            Format the response with clear section headings and keep it concise.
            Focus on what would be most helpful for someone looking for property in Kenya.
            """
            
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"LLM response generation failed: {str(e)}")
            return "I couldn't generate a response. Please check the property details directly."

    def search_and_recommend_properties(self, location: str, user_query: Optional[str] = None) -> Dict[str, Any]:
        """Main function to search, process, and recommend properties"""
        try:
            self.validate_inputs(location)
            
            # Step 1: Search for properties
            raw_properties = self.search_properties(location)
            if not raw_properties:
                return {
                    "status": "success",
                    "message": f"No properties found in {location}",
                    "properties": [],
                    "recommendations": []
                }
            
            # Process the raw data
            processed_properties = self.process_property_data(raw_properties)
            
            # Generate recommendations
            recommendations = self.generate_recommendations(processed_properties)
            
            # Create LLM response
            llm_response = self.create_llm_response(processed_properties, user_query)
            
            return {
                "status": "success",
                "location": location,
                "properties": processed_properties,
                "recommendations": recommendations,
                "llm_response": llm_response
            }
            
        except Exception as e:
            logger.error(f"Property search failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "properties": [],
                "recommendations": []
            }
