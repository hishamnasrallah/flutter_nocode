# =====================================
# File: core/api/mock/marketplace/support_views.py
"""
Marketplace Support & Miscellaneous Mock API Views
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data import CompleteMarketplaceMockData

marketplace_mock = CompleteMarketplaceMockData()


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_faqs(request):
    """Get FAQs"""
    all_data = marketplace_mock.get_data_sources()
    faqs = all_data.get('FAQs', [])
    return JsonResponse(faqs, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_notifications(request):
    """Get user notifications"""
    all_data = marketplace_mock.get_data_sources()
    notifications = all_data.get('Notifications', [])
    return JsonResponse(notifications, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_coupons(request):
    """Get available coupons"""
    all_data = marketplace_mock.get_data_sources()
    coupons = all_data.get('Coupons', [])
    return JsonResponse(coupons, safe=False)
