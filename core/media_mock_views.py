"""
Mock Media Upload API Views
File: core/media_mock_views.py
"""

import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def mock_upload_file(request):
    """Mock file upload endpoint"""
    # In real implementation, would handle request.FILES

    return JsonResponse({
        "success": True,
        "file": {
            "id": str(uuid.uuid4()),
            "url": f"https://picsum.photos/400/400?random={uuid.uuid4().hex}",
            "filename": "uploaded_image.jpg",
            "size": 125000,
            "type": "image/jpeg"
        }
    })


@csrf_exempt
@require_http_methods(["POST"])
def mock_upload_multiple(request):
    """Mock multiple file upload"""
    files = []

    for i in range(3):
        files.append({
            "id": str(uuid.uuid4()),
            "url": f"https://picsum.photos/400/400?random={uuid.uuid4().hex}",
            "filename": f"image_{i + 1}.jpg",
            "size": 125000 + (i * 1000),
            "type": "image/jpeg"
        })

    return JsonResponse({
        "success": True,
        "files": files
    })


@csrf_exempt
@require_http_methods(["DELETE"])
def mock_delete_file(request, file_id):
    """Mock file deletion"""
    return JsonResponse({
        "success": True,
        "message": f"File {file_id} deleted successfully"
    })