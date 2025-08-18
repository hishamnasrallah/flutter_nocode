# =====================================
# File: core/api/mock/chat/views.py
"""
Chat System Mock API Views
Provides mock chat and messaging endpoints
"""

import json
import uuid
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["GET"])
def mock_conversations(request):
    """Mock conversations list"""
    conversations = []

    for i in range(5):
        conversations.append({
            "id": f"conv_{i}",
            "participant": {
                "id": f"user_{i}",
                "name": f"Seller {i + 1}",
                "avatar": f"https://picsum.photos/50/50?random=seller{i}",
                "online": i % 2 == 0
            },
            "last_message": "Thanks for your interest in this product!",
            "last_message_time": (datetime.now() - timedelta(hours=i)).isoformat(),
            "unread_count": i % 3
        })

    return JsonResponse(conversations, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def mock_messages(request, conversation_id):
    """Mock messages in a conversation"""
    messages = []

    sample_messages = [
        ("Hello, is this item still available?", "user"),
        ("Yes, it's available! Would you like more details?", "seller"),
        ("What's the condition like?", "user"),
        ("It's in excellent condition, barely used.", "seller"),
        ("Great! Can you do $50?", "user"),
        ("I can do $55, that's my best price.", "seller"),
        ("Deal! How do we proceed?", "user"),
        ("Perfect! You can place the order through the app.", "seller")
    ]

    for i, (text, sender) in enumerate(sample_messages):
        messages.append({
            "id": f"msg_{i}",
            "conversation_id": conversation_id,
            "sender": sender,
            "content": text,
            "timestamp": (datetime.now() - timedelta(minutes=len(sample_messages) - i)).isoformat(),
            "is_read": True
        })

    return JsonResponse(messages, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def mock_send_message(request):
    """Mock send message endpoint"""
    data = json.loads(request.body)

    return JsonResponse({
        "success": True,
        "message": {
            "id": str(uuid.uuid4()),
            "conversation_id": data.get("conversation_id"),
            "sender": "user",
            "content": data.get("content"),
            "timestamp": datetime.now().isoformat(),
            "is_read": False
        }
    })

