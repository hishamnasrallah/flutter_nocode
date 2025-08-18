# File: core/mock_data/weather_mock_data.py
"""
Weather application mock data provider
"""

from .base_mock_data import BaseMockData
import random
from datetime import datetime, timedelta


class WeatherMockData(BaseMockData):
    """Mock data provider for weather application"""

    def __init__(self):
        self.current_weather = self._generate_current_weather()
        self.forecast = self._generate_forecast()
        self.hourly_forecast = self._generate_hourly_forecast()
        self.locations = self._generate_locations()
        self.alerts = self._generate_alerts()
        self.air_quality = self._generate_air_quality()
        self.user_profile = self._generate_user_profile()
        self.subscription_plans = self._generate_subscription_plans()
        self.weather_maps = self._generate_weather_maps()

    def get_data_sources(self):
        """Return all data sources"""
        return {
            "current_weather": self.current_weather,
            "forecast": self.forecast,
            "hourly_forecast": self.hourly_forecast,
            "locations": self.locations,
            "alerts": self.alerts,
            "air_quality": self.air_quality,
            "user_profile": self.user_profile,
            "subscription_plans": self.subscription_plans,
            "weather_maps": self.weather_maps,
        }

    def get_sample_images(self):
        """Return sample images for weather application"""
        return {
            "weather_icons": [
                "https://openweathermap.org/img/wn/01d@2x.png",  # Clear sky day
                "https://openweathermap.org/img/wn/01n@2x.png",  # Clear sky night
                "https://openweathermap.org/img/wn/02d@2x.png",  # Few clouds day
                "https://openweathermap.org/img/wn/02n@2x.png",  # Few clouds night
                "https://openweathermap.org/img/wn/03d@2x.png",  # Scattered clouds
                "https://openweathermap.org/img/wn/04d@2x.png",  # Broken clouds
                "https://openweathermap.org/img/wn/09d@2x.png",  # Shower rain
                "https://openweathermap.org/img/wn/10d@2x.png",  # Rain day
                "https://openweathermap.org/img/wn/10n@2x.png",  # Rain night
                "https://openweathermap.org/img/wn/11d@2x.png",  # Thunderstorm
                "https://openweathermap.org/img/wn/13d@2x.png",  # Snow
                "https://openweathermap.org/img/wn/50d@2x.png",  # Mist
            ],
            "backgrounds": [
                "https://picsum.photos/800/400?random=sunny",
                "https://picsum.photos/800/400?random=cloudy",
                "https://picsum.photos/800/400?random=rainy",
                "https://picsum.photos/800/400?random=stormy",
                "https://picsum.photos/800/400?random=snowy",
                "https://picsum.photos/800/400?random=foggy",
            ],
            "map_overlays": [
                "https://tile.openweathermap.org/map/temp_new/2/1/1.png",
                "https://tile.openweathermap.org/map/precipitation_new/2/1/1.png",
                "https://tile.openweathermap.org/map/wind_new/2/1/1.png",
                "https://tile.openweathermap.org/map/clouds_new/2/1/1.png",
            ],
            "location_images": [
                f"https://picsum.photos/400/300?random=city{i}" for i in range(1, 11)
            ],
            "avatars": [
                f"https://picsum.photos/150/150?random=avatar{i}" for i in range(1, 6)
            ],
        }

    def get_sample_images(self):
        """Return sample images for weather application"""
        return {
            "weather_icons": [
                "https://openweathermap.org/img/wn/01d@2x.png",  # Clear sky day
                "https://openweathermap.org/img/wn/01n@2x.png",  # Clear sky night
                "https://openweathermap.org/img/wn/02d@2x.png",  # Few clouds day
                "https://openweathermap.org/img/wn/02n@2x.png",  # Few clouds night
                "https://openweathermap.org/img/wn/03d@2x.png",  # Scattered clouds
                "https://openweathermap.org/img/wn/04d@2x.png",  # Broken clouds
                "https://openweathermap.org/img/wn/09d@2x.png",  # Shower rain
                "https://openweathermap.org/img/wn/10d@2x.png",  # Rain day
                "https://openweathermap.org/img/wn/10n@2x.png",  # Rain night
                "https://openweathermap.org/img/wn/11d@2x.png",  # Thunderstorm
                "https://openweathermap.org/img/wn/13d@2x.png",  # Snow
                "https://openweathermap.org/img/wn/50d@2x.png",  # Mist
            ],
            "backgrounds": [
                "https://picsum.photos/800/400?random=sunny",
                "https://picsum.photos/800/400?random=cloudy",
                "https://picsum.photos/800/400?random=rainy",
                "https://picsum.photos/800/400?random=stormy",
                "https://picsum.photos/800/400?random=snowy",
                "https://picsum.photos/800/400?random=foggy",
            ],
            "map_overlays": [
                "https://tile.openweathermap.org/map/temp_new/2/1/1.png",
                "https://tile.openweathermap.org/map/precipitation_new/2/1/1.png",
                "https://tile.openweathermap.org/map/wind_new/2/1/1.png",
                "https://tile.openweathermap.org/map/clouds_new/2/1/1.png",
            ],
            "location_images": [
                f"https://picsum.photos/400/300?random=city{i}" for i in range(1, 11)
            ],
            "avatars": [
                f"https://picsum.photos/150/150?random=avatar{i}" for i in range(1, 6)
            ],
        }

    def _generate_current_weather(self):
        """Generate current weather data"""
        weather_conditions = [
            "Clear", "Partly Cloudy", "Cloudy", "Overcast",
            "Light Rain", "Moderate Rain", "Heavy Rain",
            "Thunderstorm", "Snow", "Fog", "Windy"
        ]

        return {
            "location": "New York, NY",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "temperature": round(random.uniform(15, 30), 1),
            "feelsLike": round(random.uniform(14, 32), 1),
            "tempMin": round(random.uniform(10, 25), 1),
            "tempMax": round(random.uniform(20, 35), 1),
            "description": random.choice(weather_conditions),
            "humidity": random.randint(40, 80),
            "pressure": random.randint(1010, 1030),
            "windSpeed": round(random.uniform(5, 25), 1),
            "windDirection": random.randint(0, 360),
            "windGust": round(random.uniform(10, 35), 1),
            "visibility": round(random.uniform(5, 10), 1),
            "uvIndex": random.randint(1, 11),
            "cloudCover": random.randint(0, 100),
            "precipitation": round(random.uniform(0, 10), 1),
            "dewPoint": round(random.uniform(10, 20), 1),
            "icon": "cloud",
            "sunrise": "06:30",
            "sunset": "19:45",
            "moonPhase": random.choice(["New Moon", "Waxing Crescent", "First Quarter",
                                        "Waxing Gibbous", "Full Moon", "Waning Gibbous",
                                        "Last Quarter", "Waning Crescent"]),
            "lastUpdated": datetime.now().isoformat()
        }

    def _generate_forecast(self):
        """Generate 7-day forecast data"""
        forecast = []
        weather_conditions = [
            "Sunny", "Partly Cloudy", "Cloudy", "Rainy",
            "Thunderstorms", "Snowy", "Windy", "Foggy"
        ]

        for i in range(7):
            date = datetime.now() + timedelta(days=i)
            temp_min = round(random.uniform(10, 20), 1)
            temp_max = temp_min + random.uniform(5, 15)

            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "dayOfWeek": date.strftime("%A"),
                "tempMin": round(temp_min, 1),
                "tempMax": round(temp_max, 1),
                "temperature": round((temp_min + temp_max) / 2, 1),
                "description": random.choice(weather_conditions),
                "icon": random.choice(["wb_sunny", "cloud", "grain", "ac_unit"]),
                "precipitation": random.randint(0, 100),
                "humidity": random.randint(40, 90),
                "windSpeed": round(random.uniform(5, 30), 1),
                "uvIndex": random.randint(1, 11),
                "sunrise": f"06:{random.randint(15, 45):02d}",
                "sunset": f"19:{random.randint(30, 55):02d}",
                "moonPhase": random.choice(["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]),
                "airQuality": random.choice(["Good", "Moderate", "Poor"]),
            })

        return forecast

    def _generate_hourly_forecast(self):
        """Generate 24-hour forecast data"""
        hourly = []
        current_temp = round(random.uniform(15, 25), 1)
        weather_conditions = ["Clear", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain"]

        for i in range(24):
            hour = datetime.now() + timedelta(hours=i)
            # Simulate temperature changes throughout the day
            if 6 <= hour.hour <= 12:
                current_temp += random.uniform(0, 2)
            elif 12 < hour.hour <= 18:
                current_temp += random.uniform(-0.5, 1)
            else:
                current_temp -= random.uniform(0, 1.5)

            hourly.append({
                "time": hour.strftime("%H:00"),
                "hour": hour.hour,
                "temperature": round(current_temp, 1),
                "feelsLike": round(current_temp + random.uniform(-2, 2), 1),
                "description": random.choice(weather_conditions),
                "icon": random.choice(["wb_sunny", "cloud", "grain"]),
                "precipitation": random.randint(0, 70),
                "humidity": random.randint(40, 80),
                "windSpeed": round(random.uniform(5, 25), 1),
                "windDirection": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]),
                "uvIndex": random.randint(0, 11) if 6 <= hour.hour <= 18 else 0,
                "visibility": round(random.uniform(5, 10), 1),
                "pressure": random.randint(1010, 1030),
            })

        return hourly

    def _generate_locations(self):
        """Generate saved locations data"""
        locations = [
            {
                "id": "1",
                "name": "New York",
                "country": "USA",
                "countryCode": "US",
                "state": "New York",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "timezone": "America/New_York",
                "isDefault": True,
                "isCurrent": True,
                "addedDate": "2024-01-01",
                "lastViewed": datetime.now().isoformat(),
                "temperature": round(random.uniform(15, 30), 1),
                "description": "Partly Cloudy",
                "icon": "cloud",
            },
            {
                "id": "2",
                "name": "London",
                "country": "United Kingdom",
                "countryCode": "GB",
                "state": "England",
                "latitude": 51.5074,
                "longitude": -0.1278,
                "timezone": "Europe/London",
                "isDefault": False,
                "isCurrent": False,
                "addedDate": "2024-01-15",
                "lastViewed": (datetime.now() - timedelta(days=1)).isoformat(),
                "temperature": round(random.uniform(10, 20), 1),
                "description": "Rainy",
                "icon": "grain",
            },
            {
                "id": "3",
                "name": "Tokyo",
                "country": "Japan",
                "countryCode": "JP",
                "state": "Tokyo",
                "latitude": 35.6762,
                "longitude": 139.6503,
                "timezone": "Asia/Tokyo",
                "isDefault": False,
                "isCurrent": False,
                "addedDate": "2024-02-01",
                "lastViewed": (datetime.now() - timedelta(days=3)).isoformat(),
                "temperature": round(random.uniform(18, 28), 1),
                "description": "Clear",
                "icon": "wb_sunny",
            },
            {
                "id": "4",
                "name": "Paris",
                "country": "France",
                "countryCode": "FR",
                "state": "Île-de-France",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "timezone": "Europe/Paris",
                "isDefault": False,
                "isCurrent": False,
                "addedDate": "2024-02-15",
                "lastViewed": (datetime.now() - timedelta(days=5)).isoformat(),
                "temperature": round(random.uniform(12, 22), 1),
                "description": "Cloudy",
                "icon": "cloud",
            },
            {
                "id": "5",
                "name": "Sydney",
                "country": "Australia",
                "countryCode": "AU",
                "state": "New South Wales",
                "latitude": -33.8688,
                "longitude": 151.2093,
                "timezone": "Australia/Sydney",
                "isDefault": False,
                "isCurrent": False,
                "addedDate": "2024-03-01",
                "lastViewed": (datetime.now() - timedelta(days=7)).isoformat(),
                "temperature": round(random.uniform(20, 30), 1),
                "description": "Sunny",
                "icon": "wb_sunny",
            },
        ]

        return locations

    def _generate_alerts(self):
        """Generate weather alerts data"""
        alerts = []

        alert_types = [
            {
                "type": "Severe Thunderstorm",
                "severity": "Warning",
                "color": "#FFA500",
                "icon": "thunderstorm",
                "description": "Severe thunderstorms expected with damaging winds and large hail possible.",
            },
            {
                "type": "Heat Advisory",
                "severity": "Advisory",
                "color": "#FF6B6B",
                "icon": "wb_sunny",
                "description": "High temperatures expected. Take precautions to avoid heat-related illness.",
            },
            {
                "type": "Flood Watch",
                "severity": "Watch",
                "color": "#4169E1",
                "icon": "water",
                "description": "Conditions are favorable for flooding. Monitor latest weather reports.",
            },
            {
                "type": "Winter Storm",
                "severity": "Warning",
                "color": "#87CEEB",
                "icon": "ac_unit",
                "description": "Heavy snow expected. Travel will be dangerous.",
            },
        ]

        for i, alert_info in enumerate(alert_types[:2]):  # Only show 2 active alerts
            start_time = datetime.now() + timedelta(hours=random.randint(1, 6))
            end_time = start_time + timedelta(hours=random.randint(6, 24))

            alerts.append({
                "id": str(i + 1),
                "type": alert_info["type"],
                "severity": alert_info["severity"],
                "urgency": random.choice(["Immediate", "Expected", "Future"]),
                "certainty": random.choice(["Observed", "Likely", "Possible"]),
                "title": f"{alert_info['severity']}: {alert_info['type']}",
                "description": alert_info["description"],
                "instruction": "Stay tuned to local weather updates. Take necessary precautions.",
                "startTime": start_time.isoformat(),
                "endTime": end_time.isoformat(),
                "areas": ["New York", "Brooklyn", "Queens"],
                "color": alert_info["color"],
                "icon": alert_info["icon"],
                "source": "National Weather Service",
                "isActive": True,
            })

        return alerts

    def _generate_air_quality(self):
        """Generate air quality data"""
        aqi = random.randint(20, 150)

        if aqi <= 50:
            level = "Good"
            color = "#00E400"
            health_message = "Air quality is satisfactory."
        elif aqi <= 100:
            level = "Moderate"
            color = "#FFFF00"
            health_message = "Air quality is acceptable for most people."
        elif aqi <= 150:
            level = "Unhealthy for Sensitive Groups"
            color = "#FF7E00"
            health_message = "Sensitive groups may experience health effects."
        elif aqi <= 200:
            level = "Unhealthy"
            color = "#FF0000"
            health_message = "Everyone may experience health effects."
        else:
            level = "Very Unhealthy"
            color = "#8F3F97"
            health_message = "Health warnings of emergency conditions."

        return {
            "aqi": aqi,
            "level": level,
            "color": color,
            "healthMessage": health_message,
            "pm25": round(random.uniform(10, 100), 1),
            "pm10": round(random.uniform(20, 150), 1),
            "o3": round(random.uniform(30, 100), 1),
            "no2": round(random.uniform(10, 80), 1),
            "so2": round(random.uniform(5, 50), 1),
            "co": round(random.uniform(0.5, 10), 1),
            "primaryPollutant": random.choice(["PM2.5", "PM10", "Ozone"]),
            "lastUpdated": datetime.now().isoformat(),
            "forecast": [
                {"day": "Today", "aqi": aqi},
                {"day": "Tomorrow", "aqi": aqi + random.randint(-20, 20)},
                {"day": "Day After", "aqi": aqi + random.randint(-30, 30)},
            ],
        }

    def _generate_user_profile(self):
        """Generate user profile data"""
        return {
            "id": "user123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "avatar": "https://picsum.photos/150/150?random=avatar",
            "phone": "+1-555-1234",
            "memberSince": "2023-01-15",
            "preferredUnit": "metric",  # metric or imperial
            "temperatureUnit": "celsius",  # celsius or fahrenheit
            "windSpeedUnit": "km/h",  # km/h, mph, m/s
            "pressureUnit": "mb",  # mb, inHg
            "precipitationUnit": "mm",  # mm, in
            "timeFormat": "24h",  # 12h or 24h
            "language": "en",
            "notificationsEnabled": True,
            "alertsEnabled": True,
            "dailyForecastTime": "07:00",
            "theme": "light",  # light or dark
            "subscription": {
                "type": "Premium",
                "expiresAt": "2025-01-15",
                "autoRenew": True,
            },
            "favoriteLocations": ["New York", "London", "Tokyo"],
            "recentSearches": ["Paris weather", "Berlin forecast", "Rome temperature"],
            "preferences": {
                "showFeelsLike": True,
                "showHumidity": True,
                "showWindSpeed": True,
                "showUVIndex": True,
                "showAirQuality": True,
                "showPrecipitation": True,
                "showPressure": True,
                "showVisibility": True,
                "autoDetectLocation": True,
                "useGPS": True,
            },
        }

    def _generate_subscription_plans(self):
        """Generate subscription plans data"""
        return [
            {
                "id": "free",
                "name": "Free",
                "price": 0,
                "currency": "USD",
                "duration": "Forever",
                "billingCycle": "none",
                "features": [
                    "Current weather",
                    "3-day forecast",
                    "Basic weather alerts",
                    "2 saved locations",
                ],
                "limitations": [
                    "Limited to 3-day forecast",
                    "Basic weather data only",
                    "Ads included",
                ],
                "isPopular": False,
                "isCurrent": True,
                "buttonText": "Current Plan",
            },
            {
                "id": "premium_monthly",
                "name": "Premium Monthly",
                "price": 4.99,
                "currency": "USD",
                "duration": "Monthly",
                "billingCycle": "monthly",
                "features": [
                    "Everything in Free",
                    "7-day forecast",
                    "Hourly forecast for 48 hours",
                    "Advanced weather alerts",
                    "10 saved locations",
                    "Weather maps",
                    "Air quality data",
                    "No ads",
                ],
                "limitations": [],
                "isPopular": True,
                "isCurrent": False,
                "discount": 0,
                "buttonText": "Start Free Trial",
                "trialDays": 7,
            },
            {
                "id": "premium_yearly",
                "name": "Premium Yearly",
                "price": 49.99,
                "originalPrice": 59.88,
                "currency": "USD",
                "duration": "Yearly",
                "billingCycle": "yearly",
                "features": [
                    "Everything in Premium Monthly",
                    "14-day forecast",
                    "Unlimited saved locations",
                    "Historical weather data",
                    "Advanced weather maps",
                    "Precipitation radar",
                    "Hurricane tracker",
                    "Priority support",
                    "API access",
                ],
                "limitations": [],
                "isPopular": False,
                "isCurrent": False,
                "discount": 17,
                "savingsText": "Save $9.89",
                "buttonText": "Best Value",
                "trialDays": 14,
            },
            {
                "id": "professional",
                "name": "Professional",
                "price": 19.99,
                "currency": "USD",
                "duration": "Monthly",
                "billingCycle": "monthly",
                "features": [
                    "Everything in Premium",
                    "30-day forecast",
                    "API access for developers",
                    "Custom alerts",
                    "Weather data export",
                    "Team collaboration",
                    "Priority email support",
                    "Custom branding options",
                ],
                "limitations": [],
                "isPopular": False,
                "isCurrent": False,
                "buttonText": "Contact Sales",
                "isEnterprise": True,
            },
        ]

    def _generate_weather_maps(self):
        """Generate weather map configurations"""
        return {
            "availableLayers": [
                {
                    "id": "radar",
                    "name": "Radar",
                    "description": "Precipitation radar",
                    "icon": "radar",
                    "isDefault": True,
                    "isPremium": False,
                },
                {
                    "id": "satellite",
                    "name": "Satellite",
                    "description": "Cloud cover satellite imagery",
                    "icon": "satellite",
                    "isDefault": False,
                    "isPremium": False,
                },
                {
                    "id": "temperature",
                    "name": "Temperature",
                    "description": "Temperature heat map",
                    "icon": "thermostat",
                    "isDefault": False,
                    "isPremium": False,
                },
                {
                    "id": "precipitation",
                    "name": "Precipitation",
                    "description": "Expected precipitation",
                    "icon": "grain",
                    "isDefault": False,
                    "isPremium": True,
                },
                {
                    "id": "wind",
                    "name": "Wind",
                    "description": "Wind speed and direction",
                    "icon": "air",
                    "isDefault": False,
                    "isPremium": True,
                },
                {
                    "id": "pressure",
                    "name": "Pressure",
                    "description": "Atmospheric pressure",
                    "icon": "speed",
                    "isDefault": False,
                    "isPremium": True,
                },
            ],
            "mapSettings": {
                "defaultZoom": 10,
                "minZoom": 3,
                "maxZoom": 18,
                "defaultCenter": {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                },
                "animationSpeed": "normal",
                "showCityLabels": True,
                "showWeatherStations": False,
                "showGridLines": False,
            },
            "legendData": {
                "temperature": {
                    "unit": "°C",
                    "colors": [
                        {"value": -20, "color": "#0000FF"},
                        {"value": 0, "color": "#00FFFF"},
                        {"value": 20, "color": "#FFFF00"},
                        {"value": 40, "color": "#FF0000"},
                    ],
                },
                "precipitation": {
                    "unit": "mm/h",
                    "colors": [
                        {"value": 0, "color": "#FFFFFF"},
                        {"value": 1, "color": "#C6FFDD"},
                        {"value": 5, "color": "#78FF00"},
                        {"value": 10, "color": "#FFD700"},
                        {"value": 20, "color": "#FF0000"},
                    ],
                },
            },
        }

    # API response methods
    def get_current_weather(self, location=None):
        """Get current weather for a location"""
        weather = self.current_weather.copy()
        if location:
            weather["location"] = location
        return weather

    def get_forecast(self, days=7):
        """Get weather forecast"""
        return self.forecast[:days]

    def get_hourly_forecast(self, hours=24):
        """Get hourly forecast"""
        return self.hourly_forecast[:hours]

    def get_locations(self):
        """Get saved locations"""
        return self.locations

    def get_location_weather(self, location_id):
        """Get weather for a specific location"""
        for loc in self.locations:
            if loc["id"] == location_id:
                weather = self.current_weather.copy()
                weather["location"] = loc["name"]
                weather["latitude"] = loc["latitude"]
                weather["longitude"] = loc["longitude"]
                return weather
        return None

    def search_locations(self, query):
        """Search for locations"""
        cities = [
            {"name": "New York, USA", "lat": 40.7128, "lon": -74.0060},
            {"name": "Los Angeles, USA", "lat": 34.0522, "lon": -118.2437},
            {"name": "Chicago, USA", "lat": 41.8781, "lon": -87.6298},
            {"name": "Houston, USA", "lat": 29.7604, "lon": -95.3698},
            {"name": "Phoenix, USA", "lat": 33.4484, "lon": -112.0740},
            {"name": "London, UK", "lat": 51.5074, "lon": -0.1278},
            {"name": "Paris, France", "lat": 48.8566, "lon": 2.3522},
            {"name": "Tokyo, Japan", "lat": 35.6762, "lon": 139.6503},
            {"name": "Sydney, Australia", "lat": -33.8688, "lon": 151.2093},
            {"name": "Dubai, UAE", "lat": 25.2048, "lon": 55.2708},
        ]

        results = []
        query_lower = query.lower()
        for city in cities:
            if query_lower in city["name"].lower():
                results.append(city)

        return results[:5]  # Return max 5 results

    def get_alerts(self):
        """Get weather alerts"""
        return self.alerts

    def get_air_quality(self, location=None):
        """Get air quality data"""
        return self.air_quality

    def get_user_profile(self):
        """Get user profile"""
        return self.user_profile

    def get_subscription_plans(self):
        """Get subscription plans"""
        return self.subscription_plans

    def get_weather_maps(self):
        """Get weather map configuration"""
        return self.weather_maps