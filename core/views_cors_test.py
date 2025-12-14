"""
CORS test endpoint to verify CORS configuration is working.
"""
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings


class CORSTestView(APIView):
    """
    Simple endpoint to test CORS configuration.
    Returns CORS configuration details.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """GET request to test CORS"""
        return Response({
            "message": "CORS is working!",
            "origin": request.META.get("HTTP_ORIGIN", "No Origin header"),
            "cors_allowed_origins": getattr(settings, "CORS_ALLOWED_ORIGINS", []),
            "method": request.method,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """POST request to test CORS"""
        return Response({
            "message": "CORS POST is working!",
            "origin": request.META.get("HTTP_ORIGIN", "No Origin header"),
            "cors_allowed_origins": getattr(settings, "CORS_ALLOWED_ORIGINS", []),
            "method": request.method,
            "data_received": request.data,
        }, status=status.HTTP_200_OK)

    def options(self, request):
        """OPTIONS request (preflight) to test CORS"""
        return Response({
            "message": "CORS preflight is working!",
            "origin": request.META.get("HTTP_ORIGIN", "No Origin header"),
            "cors_allowed_origins": getattr(settings, "CORS_ALLOWED_ORIGINS", []),
            "method": request.method,
        }, status=status.HTTP_200_OK)

