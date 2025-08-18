# File: core/api/mock/marketplace/user_views.py
"""
Marketplace User & Account Mock API Views
Handles user profile, addresses, wallet, loyalty points, etc.
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data import CompleteMarketplaceMockData

marketplace_mock = CompleteMarketplaceMockData()


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_user_profile(request):
    """Get user profile"""
    all_data = marketplace_mock.get_data_sources()
    profile = all_data.get('User Profile', {})
    if isinstance(profile, dict):
        return JsonResponse([profile], safe=False)
    return JsonResponse(profile, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_user_addresses(request):
    """Get user addresses"""
    all_data = marketplace_mock.get_data_sources()
    addresses = all_data.get('Addresses', [])
    return JsonResponse(addresses, safe=False)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def marketplace_user_cards(request):
    """Get or add payment cards"""
    if request.method == "GET":
        all_data = marketplace_mock.get_data_sources()
        cards = all_data.get('Payment Cards', [])
        return JsonResponse(cards, safe=False)

    return JsonResponse({"success": True, "message": "Card added successfully"})


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_wishlist(request):
    """Get user wishlist"""
    all_data = marketplace_mock.get_data_sources()
    wishlist = all_data.get('Wishlist', [])
    return JsonResponse(wishlist, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_recently_viewed(request):
    """Get recently viewed products"""
    all_data = marketplace_mock.get_data_sources()
    recently_viewed = all_data.get('Recently Viewed', [])
    return JsonResponse(recently_viewed, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_loyalty_points(request):
    """Get loyalty points info"""
    all_data = marketplace_mock.get_data_sources()
    loyalty_data = all_data.get('Loyalty Points', {})
    if isinstance(loyalty_data, dict):
        return JsonResponse([loyalty_data], safe=False)
    return JsonResponse(loyalty_data, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_wallet(request):
    """Get wallet information"""
    all_data = marketplace_mock.get_data_sources()
    wallet_data = all_data.get('Wallet', {})
    if isinstance(wallet_data, dict):
        return JsonResponse([wallet_data], safe=False)
    return JsonResponse(wallet_data, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_referrals(request):
    """Get referral program info"""
    all_data = marketplace_mock.get_data_sources()
    referral_data = all_data.get('Referrals', {})
    if isinstance(referral_data, dict):
        return JsonResponse([referral_data], safe=False)
    return JsonResponse(referral_data, safe=False)