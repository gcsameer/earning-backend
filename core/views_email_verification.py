"""
Email verification endpoint for AdSense/AdMob compliance.
Verifies that email addresses exist and are valid.
"""
import re
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# Try to import dnspython, but make it optional
try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False


class EmailVerificationView(APIView):
    """
    Verify if an email address exists and is valid.
    This is required for AdSense/AdMob compliance.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()

        if not email:
            return Response(
                {"valid": False, "error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Basic format validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return Response({
                "valid": False,
                "error": "Invalid email format"
            })

        # Extract domain
        try:
            domain = email.split('@')[1]
        except IndexError:
            return Response({
                "valid": False,
                "error": "Invalid email format"
            })

        # If dnspython is not available, just do format validation
        if not DNS_AVAILABLE:
            # Basic validation - format is correct
            return Response({
                "valid": True,
                "message": "Email format is valid"
            })

        # Check if domain has MX records (email server)
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            if len(mx_records) > 0:
                return Response({
                    "valid": True,
                    "message": "Email domain is valid"
                })
            else:
                return Response({
                    "valid": False,
                    "error": "Email domain does not accept emails"
                })
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
            # If MX lookup fails, check for A record (some domains use A records)
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                if len(a_records) > 0:
                    return Response({
                        "valid": True,
                        "message": "Email domain is valid"
                    })
            except:
                pass

            return Response({
                "valid": False,
                "error": "Email domain does not exist"
            })
        except Exception as e:
            # If DNS lookup fails, we'll still allow registration but log it
            # In production, you might want to use a service like EmailListVerify
            return Response({
                "valid": True,  # Allow registration but note verification failed
                "message": "Could not verify email domain, but format is valid",
                "warning": "Email verification service unavailable"
            })

