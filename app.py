import streamlit as st
import os
from modules.search_engine import PropertySearchEngine
from modules.location_extractor import LocationExtractor
from modules.interface import (
    render_header, 
    render_property_card, 
    render_recommendations,
    render_error_message,
    render_map
)

# Set page config
st.set_page_config(
    page_title="Kenya Property Finder",
    page_icon="🏠",
    layout="wide"
)

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'last_query' not in st.session_state:
    st.session_state.last_query = ""

def main():
    # Render header
    render_header()
    
    # Input section
    with st.container():
        st.subheader("Find Your Dream Property in Kenya")
        user_query = st.text_input(
            "What kind of property are you looking for?",
            placeholder="Example: Show luxury homes for sale in Westlands, Nairobi with good ratings"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            search_button = st.button("Search Properties", type="primary")
        with col2:
            if st.session_state.search_history:
                if st.button("Clear History"):
                    st.session_state.search_history = []
                    st.rerun()
    
    # Process search when button is clicked
    if search_button and user_query:
        with st.spinner("Searching for properties..."):
            # Extract location from user query
            location_extractor = LocationExtractor()
            location = location_extractor.extract_location(user_query)
            
            if not location:
                st.error("Could not identify a location in your query. Please specify a location in Kenya.")
            else:
                # Initialize search engine
                search_engine = PropertySearchEngine()
                
                # Perform search
                result = search_engine.search_and_recommend_properties(
                    location=location,
                    user_query=user_query
                )
                
                # Store in search history
                st.session_state.last_query = user_query
                if result["status"] == "success" and result["properties"]:
                    search_result = {
                        "query": user_query,
                        "location": location,
                        "timestamp": import_time(),
                        "result": result
                    }
                    st.session_state.search_history.append(search_result)
                
                # Display results
                display_search_results(result, location)
    
    # Display search history
    if st.session_state.search_history:
        with st.expander("View Search History"):
            for i, search in enumerate(reversed(st.session_state.search_history)):
                st.write(f"**{i+1}. {search['query']}** - {search['timestamp']}")
                if st.button(f"View Results #{i+1}"):
                    display_search_results(search['result'], search['location'])

def display_search_results(result, location):
    """Display search results in the UI"""
    if result["status"] == "error":
        render_error_message(result["message"])
        return
        
    if not result["properties"]:
        st.info(f"No properties found in {location}")
        return
    
    # Display LLM summary
    st.subheader(f"Property Listings in {location}")
    with st.container():
        st.markdown(result["llm_response"])
    
    # Display property listings in cards
    st.subheader("Detailed Property Listings")
    
    # Organize properties into rows of 3
    properties = result["properties"]
    
    for i in range(0, len(properties), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(properties):
                with cols[j]:
                    render_property_card(properties[i+j])
    
    # Display recommendations
    if result["recommendations"]:
        render_recommendations(result["recommendations"])
        
    # Display map with all properties
    if properties:
        render_map(properties)

def import_time():
    """Import datetime only when needed to improve startup time"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M")

if __name__ == "__main__":
    main()
