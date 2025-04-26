import re
from groq import Groq
import os
import logging
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)

class LocationExtractor:
    """Class to extract location information from user queries"""
    
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.groq_client = Groq(api_key=self.groq_api_key) if self.groq_api_key else None
        
        # Common Kenya locations for basic matching
        self.kenya_locations = [
            "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", 
            "Nyeri", "Machakos", "Malindi", "Kitui", "Garissa",
            "Westlands", "Karen", "Kilimani", "Runda", "Kileleshwa", 
            "Lavington", "Muthaiga", "Nyali", "South B", "South C"
        ]
    
    def extract_location_basic(self, text: str) -> str:
        """Simple location extraction using pattern matching"""
        text = text.lower()
        
        # Check for direct mentions of locations
        for location in self.kenya_locations:
            if location.lower() in text:
                return location
        
        # Try to find "in {location}" patterns
        in_matches = re.findall(r'in\s+([a-zA-Z0-9\s]+)(?:,\s*([a-zA-Z\s]+))?', text)
        if in_matches:
            for match in in_matches:
                location = match[0].strip()
                if match[1]:  # If there's a second part (like "Westlands, Nairobi")
                    location = f"{location}, {match[1].strip()}"
                return location
                
        return ""
    
    def extract_location_llm(self, text: str) -> str:
        """Extract location using LLM for more complex queries"""
        if not self.groq_client:
            return ""
            
        try:
            prompt = f"""
            Extract the specific location in Kenya where the user is looking for property from this query:
            "{text}"
            
            Only return the location name without any additional text or explanation.
            If no specific location in Kenya is mentioned, respond with "Unknown".
            
            For example:
            "I want a house in Westlands" -> "Westlands"
            "Show luxury apartments in Kilimani, Nairobi" -> "Kilimani, Nairobi"
            "What properties are available" -> "Unknown"
            """
            
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                temperature=0.1,
                max_tokens=50
            )
            
            location = response.choices[0].message.content.strip()
            return "" if location == "Unknown" else location
            
        except Exception as e:
            logger.error(f"LLM location extraction failed: {str(e)}")
            return ""
    
    def extract_location(self, text: str) -> str:
        """Extract location using multiple methods"""
        # First try basic matching
        location = self.extract_location_basic(text)
        
        # If that fails, try LLM-based extraction
        if not location:
            location = self.extract_location_llm(text)
            
        # If still no location, default to Nairobi
        if not location:
            return ""
            
        return location