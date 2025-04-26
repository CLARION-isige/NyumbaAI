import streamlit as st
import folium
from streamlit_folium import folium_static

def render_header():
    """Render application header"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://cdnjs.cloudflare.com/ajax/libs/emojione/2.0.1/assets/svg/1f3e0.svg", width=100)
    
    with col2:
        st.title("NyumbaAI:Kenya Property Finder")
        st.markdown("""
        Find and compare properties for sale across Kenya. 
        Get personalized recommendations and detailed information.
        """)
    
    st.divider()

def render_property_card(property_data):
    """Render individual property card"""
    with st.container():
        st.subheader(property_data["name"])
        
        # Rating stars
        rating = property_data["rating"]
        stars = "⭐" * int(rating) + ("⭐" if rating % 1 >= 0.5 else "")
        st.write(f"{stars} ({property_data['reviews']} reviews)")
        
        st.markdown(f"**Type:** {property_data['type']}")
        st.markdown(f"**Address:** {property_data['address']}")
        
        if property_data.get("description"):
            st.markdown(f"**Description:** {property_data['description']}")
        
        if property_data.get("price") and property_data["price"] != "Price not specified":
            st.markdown(f"**Price:** {property_data['price']}")
        
        if property_data.get("years_in_business"):
            st.markdown(f"**Experience:** {property_data['years_in_business']}")
        
        st.markdown(f"**Contact:** {property_data['contact']}")
        st.markdown(f"**Hours:** {property_data['hours']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if property_data.get("website"):
                st.markdown(f"[Visit Website]({property_data['website']})")
        
        with col2:
            if property_data.get("map_link"):
                st.markdown(f"[Get Directions]({property_data['map_link']})")
        
        st.divider()

def render_recommendations(recommendations):
    """Render property recommendations section"""
    st.subheader("Top Recommended Properties")
    st.write("Based on ratings, reviews, and business reputation:")
    
    for i, prop in enumerate(recommendations):
        st.write(f"{i+1}. **{prop['name']}** - {prop['rating']}⭐ ({prop['reviews']} reviews)")
        
        if prop.get("years_in_business"):
            st.write(f"   {prop['years_in_business']}")
        
        st.write(f"   Contact: {prop['contact']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if prop.get("website"):
                st.markdown(f"   [Visit Website]({prop['website']})")
        with col2:
            if prop.get("map_link"):
                st.markdown(f"   [Get Directions]({prop['map_link']})")
        
        st.write("")
    
    st.divider()

def render_error_message(message):
    """Render error message"""
    st.error(f"Error: {message}")
    
    st.markdown("""
    ### Troubleshooting:
    - Make sure you specified a location in Kenya
    - Check that your API keys are set up correctly
    - Try a different search query
    """)

def render_map(properties):
    """Render map with property locations"""
    st.subheader("Property Locations")
    
    # Create a map centered at the average location of all properties
    coordinates = [prop.get("coordinates", {}) for prop in properties if prop.get("coordinates")]
    
    if not coordinates:
        st.info("No location data available for mapping")
        return
    
    # Calculate center of the map
    total_lat = sum(coord.get("latitude", 0) for coord in coordinates if coord.get("latitude"))
    total_lng = sum(coord.get("longitude", 0) for coord in coordinates if coord.get("longitude"))
    count = sum(1 for coord in coordinates if coord.get("latitude") and coord.get("longitude"))
    
    if count == 0:
        # Default to Nairobi center
        center_lat, center_lng = -1.2921, 36.8219
    else:
        center_lat = total_lat / count
        center_lng = total_lng / count
    
    # Create map
    m = folium.Map(location=[center_lat, center_lng], zoom_start=12)
    
    # Add markers for each property
    for prop in properties:
        coord = prop.get("coordinates", {})
        if coord and coord.get("latitude") and coord.get("longitude"):
            popup_html = f"""
            <strong>{prop['name']}</strong><br>
            Rating: {prop['rating']} ⭐ ({prop['reviews']} reviews)<br>
            Contact: {prop['contact']}<br>
            """
            
            folium.Marker(
                location=[coord["latitude"], coord["longitude"]],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=prop["name"]
            ).add_to(m)
    
    # Display the map
    folium_static(m)