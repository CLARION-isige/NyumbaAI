# Background 
House hunting can be very hectic especially moving into unknown city or county coming from a personal standpoint.

This project aims to address this by, having potential tenants/home buyers search for houses in the areas of their liking, see the price range and get conttact information for further inquiry. The user also gets to see the map to the location of the houses and the website if it exists.

This aims to reduce the time people take to search for houses and ensuring a seamless experience with minimal effort.

# NyumbaAI:Kenya Property Finder

A Streamlit application for searching and comparing properties across Kenya. This application helps users find available properties, get detailed information, and receive personalized recommendations.

## Features

- Natural language property search across Kenya
- Location extraction from user queries
- Property recommendations based on ratings and reviews
- Interactive property listings with detailed information
- Interactive map visualization of property locations
- Search history tracking
- LLM-powered property summaries and recommendations using Groq

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kenya-property-finder.git
cd kenya-property-finder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables by creating a `.env` file:
```
SERP_API_KEY=your_serp_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser at `http://localhost:8501`

3. Enter your property search query in the text area, including location and preferences:
   - Example: "Show luxury homes for sale in Westlands, Nairobi with good ratings"
   - Example: "Find affordable apartments in Kilimani with at least 2 bedrooms"
   - Example: "Houses for sale in Karen with swimming pools"

4. View property listings, recommendations, and map visualization

## Project Structure

```
kenya-property-finder/
├── app.py                  # Main Streamlit application
├── modules/
│   ├── search_engine.py    # Property search functionality
│   ├── location_extractor.py # Location extraction from queries
│   └── ui_components.py    # UI components for Streamlit
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (create this file)
└── README.md               # Project documentation
```

## API Keys

This application requires:
- SERP API key: For property search data
- Groq API key: For natural language processing

Get your API keys from:
- SERP API: https://serpapi.com/
- Groq: https://console.groq.com/

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
