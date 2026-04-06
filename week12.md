# 🧩 API Integration in Django (External APIs)
## 🎯 Intended Learning Outcomes (ILOs)
By the end of this lesson, students should be able to:
**Explain** the principles of REST and JSON data exchange.
**Access** data from public APIs (e.g., NASA API, Weather API).
**Parse** JSON responses and **display** data in Django templates.
**Implement** error handling for failed API requests.
## 🗂️ API Overview
API integration allows web applications to **communicate with external services** — such as weather data, space imagery, or currency exchange — using **RESTful APIs** and **JSON** as the common data format.
In Django, this is typically done through the **`requests`** library and displayed dynamically in templates.
## 🌐 REST Fundamentals
### 🔹 What is REST?
**REST (Representational State Transfer)** is an architectural style for designing web services that communicate over HTTP.
A RESTful API allows clients (like your Django app) to perform actions using standard HTTP methods.
| HTTP Method | Description | Example Use Case |
|---|---|---|
| **GET** | Retrieve data | Get weather data |
| **POST** | Create new data | Submit a form |
| **PUT** | Update existing data | Edit a user profile |
| **DELETE** | Remove data | Delete a record |
### 🔹 REST Endpoints
An **endpoint** is a specific URL that represents a resource that an API provides access to.
For OpenWeather, one common resource is **current weather data** for a specific city.
**Example:**
```
  https://api.openweathermap.org/data/2.5/weather?q=Manila&appid=YOUR_API_KEY&units=metric
```
**Base URL:**
```
  https://api.openweathermap.org/data/2.5/weather
```
**Query Parameters:**
`q=Manila` → the city name
`appid=YOUR_API_KEY` → your unique API key from OpenWeather
`units=metric` → optional, sets temperature to Celsius (default is Kelvin)
### 🔹 JSON Data Format
**JSON (JavaScript Object Notation)** is a lightweight format for exchanging data between a client and a server.
When we request weather information from the OpenWeather API, it responds with a JSON object containing structured weather data.
**Example JSON response:**
```
  {
  "coord": { "lon": 120.98, "lat": 14.6 },
  "weather": [
    {
      "id": 802,
      "main": "Clouds",
      "description": "scattered clouds",
      "icon": "03d"
    }
  ],
  "main": {
    "temp": 30.2,
    "feels_like": 33.1,
    "humidity": 70
  },
  "name": "Manila"
  }
```
✅ **Explanation:**
`"coord"` → coordinates of the city
`"weather"` → description of current weather conditions
`"main"` → temperature, humidity, and other atmospheric data
`"name"` → name of the city
JSON is **easy to parse in Python** using libraries like `requests` and `json`, and its data can be **passed directly to Django templates** for dynamic display.
## ☁️ Using Third-Party APIs
Common examples of public APIs:
🌌 **NASA API** – Astronomy Picture of the Day
🌦️ **Weather API** – Real-time weather information
💳 **Payment APIs** – Stripe, PayPal, etc.
# 🌦 Django OpenWeather App
This activity will help you create a simple **Weather Dashboard** using **Django** and the **OpenWeather API**.
## 🧩 1. Clone the Project Repository
Open your terminal and run:
```
  git clone https://github.com/CC6-Pancake/openweather.git
  cd openweather
```
This will download the starter Django project to your machine.
## 📦 2. Install Dependencies
Once inside the project folder, install all the required Python packages:
```
  pip install -r requirements.txt
```
This will install:
`Django`
`requests`
`python-dotenv`
## 🌍 3. Create an OpenWeather Account and API Key
Go to 👉 [https://openweathermap.org/](https://openweathermap.org/)
Click **Sign Up** and create your free account.
After logging in, go to your API Keys page .
Copy your **API key**.
⚠️ Note: It may take up to **1 hour** for a new key to activate.
## 🔑 4. Create a  `.env`  File
Inside the **project root directory** (same level as `manage.py`), create a file named:
```
  .env
```
Add this line inside the file (replace with your own key):
```
  OPENWEATHER_API_KEY=your_openweather_api_key_here
```
✅ **Tip:** Don’t put quotation marks or spaces around the key.
## ⚙️ 5. Check Django Settings
In `projectsite/settings.py`, make sure these lines are present to load your `.env` file and templates:
```
  import os
  from dotenv import load_dotenv
  
  load_dotenv()
  
  TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
  ]
```
## 🗺️ 6. Review URL Configuration
File: `projectsite/urls.py`
```
  from django.contrib import admin
  from django.urls import path
  from weather import views
  
  urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.weather_view, name='weather'),
  ]
```
## 🌦 7. Review the View Logic
File: `weather/views.py`
```
  from django.shortcuts import render
  import os
  import requests
  def weather_view(request):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    print("API Key:", os.getenv("OPENWEATHER_API_KEY"))
    city = request.GET.get("city", "Puerto Princesa")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    weather_data = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
        }
    except requests.exceptions.RequestException as e:
        weather_data = {
            "error": "Failed to fetch weather data",
            "details": str(e),
        }
    except KeyError:
        weather_data = {
            "error": f"Could not find weather information for '{city}'."
        }
    return render(request, "weather.html", {"weather": weather_data, "city": city})
```
## 🖼️ 8. Review the Template
File: `templates/weather.html`
```
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Weather Dashboard</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2em; text-align: center; }
      img { max-width: 80%; border-radius: 10px; margin-top: 1em; }
      .error { color: red; }
    </style>
  </head>
  <body>
    <h1>Weather Dashboard</h1>
    <form method="get">
      <input type="text" name="city" placeholder="Enter city name" value="{{ city }}" />
      <button type="submit">Search</button>
    </form>
  	{% if weather.error %}
      <p class="error">{{ weather.error }}</p>
      {% if weather.details %}
        <pre>{{ weather.details }}</pre>
      {% endif %}
    {% else %}
      <h2>{{ weather.city }}, {{ weather.country }}</h2>
      <p><img src="https://openweathermap.org/img/wn/{{ weather.icon }}@2x.png" alt="icon" /></p>
      <p><strong>{{ weather.temp }} °C</strong></p>
      <p>{{ weather.description }}</p>
    {% endif %}
  </body>
  </html>
```
## 🚀 9. Run the Django Server
In your terminal, from the project folder, run:
```
  python manage.py runserver
```
Then open your browser and go to:
```
  http://127.0.0.1:8000/
```
You’ll see the **Weather Dashboard**!
Type a city name (e.g., *Manila*, *Tokyo*, *New York*) and press **Search** 🌤️
## ✅ 10. Expected Output
When successful, the app will display:
City and country
Temperature (°C)
Weather description
Weather icon
If something goes wrong (e.g., invalid key or no internet), an error message will appear in red.
## References
Current weather data: https://openweathermap.org/current
