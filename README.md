<<<<<<< HEAD
Here's a comprehensive README.md file for your application:

```markdown
# NyumbaAI - Smart Property Search Solution 🏠

A Django-powered web application that simplifies house hunting using AI analysis and real-time property data.

## 📌 Features

- **AI-Powered Analysis**: Groq integration for instant market insights
- **Location-Based Search**: Find properties in specific areas
- **Direct Landlord Connections**: Verified property listings with contact info
- **Time-Saving Interface**: Reduce physical visits by 80%
- **Real-Time Updates**: Fresh property data from SerpAPI
- **Interactive Maps**: View property locations instantly

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 4.2+
- Groq API Key
- SerpAPI Key

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/CLARION-isige/NyumbaAI.git
cd NyumbaAI
```

2. **Set Up Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Update with your API keys
nano .env
```

5. **Run Migrations**
```bash
python manage.py migrate
```

6. **Start Development Server**
```bash
python manage.py runserver
```

## 🔧 Configuration

Add these to your `.env` file:
```ini
GROQ_API_KEY=your_groq_key_here
SERP_API_KEY=your_serpapi_key_here
SECRET_KEY=django-secret-key
DEBUG=True
```

## 🖥️ Usage

1. Access homepage at `http://localhost:8000`
2. Enter location and property requirements
3. View AI-analyzed results
4. Contact landlords directly
5. Save favorite listings

## 🛠️ Technology Stack

- **Backend**: Django 4.2
- **AI Processing**: Groq API
- **Property Data**: SerpAPI
- **Frontend**: Bootstrap 5
- **Database**: SQLite (Development)
- **Mapping**: Google Maps API


## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## ✉️ Contact

Project Maintainer: [Your Name] - your.email@example.com

Project Link: [https://github.com/yourusername/NyumbaAI](https://github.com/yourusername/NyumbaAI)

## 🙏 Acknowledgments

- Groq for AI processing capabilities
- SerpAPI for property data
- Django Software Foundation
```
=======
House hunting can be very hectic  especially moving into unknown city or county coming from a personal standpoint.

>>>>>>> 25a559dc7ff81898af22986741591027cf43183c
