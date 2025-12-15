"""
Admin API views for managing withdrawal requests.
These endpoints require admin/staff permissions.
"""
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db import transaction

from .models import WithdrawRequest, Settings
from .serializers import WithdrawRequestSerializer


class AdminWithdrawListView(APIView):
    """
    List all withdrawal requests (admin only).
    GET /api/admin/withdraws/
    """
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Get filter parameters
        status_filter = request.query_params.get('status', None)
        method_filter = request.query_params.get('method', None)
        
        # Base queryset
        queryset = WithdrawRequest.objects.select_related('user').order_by('-created_at')
        
        # Apply filters
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if method_filter:
            queryset = queryset.filter(method=method_filter)
        
        # Serialize and return
        serializer = WithdrawRequestSerializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "results": serializer.data
        })


class AdminWithdrawDetailView(APIView):
    """
    Get, approve, reject, or mark as paid a withdrawal request (admin only).
    GET /api/admin/withdraws/<id>/
    POST /api/admin/withdraws/<id>/approve/
    POST /api/admin/withdraws/<id>/reject/
    POST /api/admin/withdraws/<id>/mark-paid/
    """
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, withdraw_id):
        try:
            withdraw = WithdrawRequest.objects.select_related('user').get(id=withdraw_id)
            serializer = WithdrawRequestSerializer(withdraw)
            return Response(serializer.data)
        except WithdrawRequest.DoesNotExist:
            return Response(
                {"detail": "Withdrawal request not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def post(self, request, withdraw_id, action):
        """
        Handle approve, reject, or mark-paid actions
        """
        try:
            withdraw = WithdrawRequest.objects.select_related('user').get(id=withdraw_id)
        except WithdrawRequest.DoesNotExist:
            return Response(
                {"detail": "Withdrawal request not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if action == 'approve':
            if withdraw.status != WithdrawRequest.STATUS_PENDING:
                return Response(
                    {"detail": f"Can only approve pending requests. Current status: {withdraw.status}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            withdraw.status = WithdrawRequest.STATUS_APPROVED
            withdraw.processed_at = timezone.now()
            withdraw.admin_note = request.data.get('admin_note', withdraw.admin_note)
            withdraw.save()
            
            return Response({
                "message": "Withdrawal request approved",
                "withdraw": WithdrawRequestSerializer(withdraw).data
            })
        
        elif action == 'reject':
            if withdraw.status != WithdrawRequest.STATUS_PENDING:
                return Response(
                    {"detail": f"Can only reject pending requests. Current status: {withdraw.status}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Refund coins to user
            rate = float(Settings.get_value("COIN_TO_RS_RATE", "0.1"))
            coins_to_refund = int(float(withdraw.amount_rs) / rate)
            
            with transaction.atomic():
                withdraw.user.coins_balance += coins_to_refund
                withdraw.user.save(update_fields=["coins_balance"])
                
                withdraw.status = WithdrawRequest.STATUS_REJECTED
                withdraw.processed_at = timezone.now()
                withdraw.admin_note = request.data.get('admin_note', withdraw.admin_note)
                withdraw.save()
            
            return Response({
                "message": "Withdrawal request rejected and coins refunded",
                "coins_refunded": coins_to_refund,
                "withdraw": WithdrawRequestSerializer(withdraw).data
            })
        
        elif action == 'mark-paid':
            if withdraw.status != WithdrawRequest.STATUS_APPROVED:
                return Response(
                    {"detail": f"Can only mark approved requests as paid. Current status: {withdraw.status}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            withdraw.status = WithdrawRequest.STATUS_PAID
            withdraw.processed_at = timezone.now()
            withdraw.admin_note = request.data.get('admin_note', withdraw.admin_note)
            withdraw.save()
            
            return Response({
                "message": "Withdrawal request marked as paid",
                "withdraw": WithdrawRequestSerializer(withdraw).data
            })
        
        else:
            return Response(
                {"detail": f"Invalid action: {action}. Use 'approve', 'reject', or 'mark-paid'"},
                status=status.HTTP_400_BAD_REQUEST
            )

