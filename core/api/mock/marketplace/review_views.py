# =====================================
# File: core/api/mock/marketplace/review_views.py
"""
Marketplace Review & Rating Mock API Views
"""

import json
import uuid
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data import CompleteMarketplaceMockData

marketplace_mock = CompleteMarketplaceMockData()


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_reviews(request):
    """Get all reviews"""
    all_data = marketplace_mock.get_data_sources()
    reviews = all_data.get('Reviews', [])
    return JsonResponse(reviews, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_product_reviews(request, product_id):
    """Get reviews for a specific product"""
    all_data = marketplace_mock.get_data_sources()
    reviews = all_data.get('Reviews', [])

    product_reviews = [r for r in reviews if r.get('productId') == product_id]
    return JsonResponse(product_reviews, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def marketplace_add_review(request):
    """Add a product review"""
    data = json.loads(request.body)

    review = {
        "id": str(uuid.uuid4()),
        "productId": data.get('productId'),
        "rating": data.get('rating', 5),
        "title": data.get('title', ''),
        "comment": data.get('comment', ''),
        "userName": data.get('userName', 'Anonymous'),
        "date": datetime.now().isoformat(),
        "helpful": 0,
        "verified": True
    }

    return JsonResponse({"success": True, "review": review})

