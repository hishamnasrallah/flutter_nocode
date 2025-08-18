# File: core/api/mock/weather/views.py
"""
Mock API views for Weather application
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data.weather_mock_data import WeatherMockData
import json
from datetime import datetime, timedelta
import random

# Initialize mock data
weather_data = WeatherMockData()


@csrf_exempt
@require_http_methods(["GET"])
def get_current_weather(request):
    """Get current weather data"""
    location = request.GET.get('location', 'New York, NY')
    units = request.GET.get('units', 'metric')

    weather = weather_data.get_current_weather(location)

    # Convert units if imperial requested
    if units == 'imperial':
        weather['temperature'] = round(weather['temperature'] * 9 / 5 + 32, 1)
        weather['feelsLike'] = round(weather['feelsLike'] * 9 / 5 + 32, 1)
        weather['tempMin'] = round(weather['tempMin'] * 9 / 5 + 32, 1)
        weather['tempMax'] = round(weather['tempMax'] * 9 / 5 + 32, 1)
        weather['windSpeed'] = round(weather['windSpeed'] * 0.621371, 1)
        weather['unit'] = 'F'
    else:
        weather['unit'] = 'C'

    return JsonResponse(weather)


@csrf_exempt
@require_http_methods(["GET"])
def get_forecast(request):
    """Get weather forecast"""
    days = int(request.GET.get('days', 7))
    location = request.GET.get('location', 'New York, NY')
    units = request.GET.get('units', 'metric')

    forecast = weather_data.get_forecast(days)

    # Convert units if imperial requested
    if units == 'imperial':
        for day in forecast:
            day['tempMin'] = round(day['tempMin'] * 9 / 5 + 32, 1)
            day['tempMax'] = round(day['tempMax'] * 9 / 5 + 32, 1)
            day['temperature'] = round(day['temperature'] * 9 / 5 + 32, 1)
            day['windSpeed'] = round(day['windSpeed'] * 0.621371, 1)

    return JsonResponse({
        'location': location,
        'days': days,
        'units': units,
        'forecast': forecast
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_hourly_forecast(request):
    """Get hourly weather forecast"""
    hours = int(request.GET.get('hours', 24))
    location = request.GET.get('location', 'New York, NY')
    units = request.GET.get('units', 'metric')

    hourly = weather_data.get_hourly_forecast(hours)

    # Convert units if imperial requested
    if units == 'imperial':
        for hour in hourly:
            hour['temperature'] = round(hour['temperature'] * 9 / 5 + 32, 1)
            hour['feelsLike'] = round(hour['feelsLike'] * 9 / 5 + 32, 1)
            hour['windSpeed'] = round(hour['windSpeed'] * 0.621371, 1)

    return JsonResponse({
        'location': location,
        'hours': hours,
        'units': units,
        'hourly': hourly
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_locations(request):
    """Get saved locations"""
    locations = weather_data.get_locations()
    return JsonResponse({
        'count': len(locations),
        'locations': locations
    })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_location(request, location_id=None):
    """Manage a specific location"""
    if request.method == "GET":
        if location_id:
            weather = weather_data.get_location_weather(location_id)
            if weather:
                return JsonResponse(weather)
            return JsonResponse({'error': 'Location not found'}, status=404)
        else:
            return get_locations(request)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            # In a real app, this would save to database
            return JsonResponse({
                'success': True,
                'message': 'Location saved',
                'location': {
                    'id': str(random.randint(100, 999)),
                    'name': data.get('name'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'addedDate': datetime.now().isoformat()
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def search_locations(request):
    """Search for locations"""
    query = request.GET.get('q', '')

    if not query:
        return JsonResponse({'error': 'Query parameter required'}, status=400)

    results = weather_data.search_locations(query)

    return JsonResponse({
        'query': query,
        'count': len(results),
        'results': results
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_alerts(request):
    """Get weather alerts"""
    location = request.GET.get('location', 'New York, NY')
    active_only = request.GET.get('active', 'true').lower() == 'true'

    alerts = weather_data.get_alerts()

    if active_only:
        alerts = [a for a in alerts if a.get('isActive', True)]

    return JsonResponse({
        'location': location,
        'count': len(alerts),
        'alerts': alerts
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_air_quality(request):
    """Get air quality data"""
    location = request.GET.get('location', 'New York, NY')

    air_quality = weather_data.get_air_quality(location)

    return JsonResponse({
        'location': location,
        'data': air_quality
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_weather_maps(request):
    """Get weather map configuration and data"""
    map_type = request.GET.get('type', 'radar')

    maps_config = weather_data.get_weather_maps()

    # Add current map data URL
    maps_config['currentMapUrl'] = f"/api/mock/weather/maps/{map_type}/tiles"
    maps_config['selectedLayer'] = map_type

    return JsonResponse(maps_config)


@csrf_exempt
@require_http_methods(["GET"])
def get_map_tiles(request, map_type):
    """Get map tiles for specific weather layer"""
    zoom = request.GET.get('z', 10)
    x = request.GET.get('x', 0)
    y = request.GET.get('y', 0)

    # In a real app, this would return actual map tile data
    return JsonResponse({
        'type': map_type,
        'tile': {
            'x': x,
            'y': y,
            'z': zoom,
            'url': f"https://tile.openweathermap.org/map/{map_type}/{zoom}/{x}/{y}.png"
        }
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_user_profile(request):
    """Get user profile and preferences"""
    profile = weather_data.get_user_profile()
    return JsonResponse(profile)


@csrf_exempt
@require_http_methods(["POST", "PUT"])
def update_user_profile(request):
    """Update user profile and preferences"""
    try:
        data = json.loads(request.body)
        # In a real app, this would update the database
        profile = weather_data.get_user_profile()
        profile.update(data)

        return JsonResponse({
            'success': True,
            'message': 'Profile updated',
            'profile': profile
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def get_subscription_plans(request):
    """Get available subscription plans"""
    plans = weather_data.get_subscription_plans()

    return JsonResponse({
        'count': len(plans),
        'plans': plans
    })


@csrf_exempt
@require_http_methods(["POST"])
def subscribe(request):
    """Subscribe to a plan"""
    try:
        data = json.loads(request.body)
        plan_id = data.get('planId')

        # In a real app, this would process payment and update subscription
        return JsonResponse({
            'success': True,
            'message': 'Subscription successful',
            'subscription': {
                'planId': plan_id,
                'startDate': datetime.now().isoformat(),
                'endDate': (datetime.now() + timedelta(days=30)).isoformat(),
                'status': 'active'
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """User login"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        # Mock authentication
        if email and password:
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': 'user123',
                    'email': email,
                    'name': 'John Doe',
                    'token': 'mock_jwt_token_' + str(random.randint(1000, 9999))
                }
            })

        return JsonResponse({
            'success': False,
            'message': 'Invalid credentials'
        }, status=401)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """User registration"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if email and password and name:
            return JsonResponse({
                'success': True,
                'message': 'Registration successful',
                'user': {
                    'id': 'user' + str(random.randint(1000, 9999)),
                    'email': email,
                    'name': name,
                    'token': 'mock_jwt_token_' + str(random.randint(1000, 9999))
                }
            })

        return JsonResponse({
            'success': False,
            'message': 'All fields are required'
        }, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def forgot_password(request):
    """Password reset request"""
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if email:
            return JsonResponse({
                'success': True,
                'message': f'Password reset link sent to {email}'
            })

        return JsonResponse({
            'success': False,
            'message': 'Email is required'
        }, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    """Change user password"""
    try:
        data = json.loads(request.body)
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')

        if current_password and new_password:
            return JsonResponse({
                'success': True,
                'message': 'Password changed successfully'
            })

        return JsonResponse({
            'success': False,
            'message': 'Current and new password are required'
        }, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def send_support_message(request):
    """Send support/contact message"""
    try:
        data = json.loads(request.body)
        subject = data.get('subject')
        message = data.get('message')
        email = data.get('email', 'user@example.com')

        if subject and message:
            return JsonResponse({
                'success': True,
                'message': 'Your message has been sent. We will respond within 24 hours.',
                'ticketId': 'TICKET-' + str(random.randint(10000, 99999))
            })

        return JsonResponse({
            'success': False,
            'message': 'Subject and message are required'
        }, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def test_connection(request):
    """Test API connection"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Weather API is running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_weather_stats(request):
    """Get weather statistics and trends"""
    location = request.GET.get('location', 'New York, NY')

    # Generate mock statistics
    stats = {
        'location': location,
        'period': '30 days',
        'avgTemperature': round(random.uniform(15, 25), 1),
        'maxTemperature': round(random.uniform(28, 35), 1),
        'minTemperature': round(random.uniform(5, 15), 1),
        'totalRainfall': round(random.uniform(20, 100), 1),
        'sunnyDays': random.randint(10, 20),
        'rainyDays': random.randint(5, 15),
        'avgHumidity': random.randint(50, 70),
        'avgWindSpeed': round(random.uniform(10, 20), 1),
        'trends': {
            'temperature': random.choice(['increasing', 'decreasing', 'stable']),
            'rainfall': random.choice(['above average', 'below average', 'normal']),
        }
    }

    return JsonResponse(stats)