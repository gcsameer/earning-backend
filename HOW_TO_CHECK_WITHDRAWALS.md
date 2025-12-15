# 📋 How to Check Withdrawal Requests

There are **3 ways** to check withdrawal requests:

---

## Method 1: Django Admin Panel (Easiest) ⭐

### Step 1: Access Admin Panel
1. Go to: `https://your-backend.railway.app/admin/`
2. Login with your **superuser** credentials

### Step 2: View Withdrawal Requests
1. Click on **"Withdraw requests"** in the admin panel
2. You'll see all withdrawal requests with:
   - User
   - Amount (Rs)
   - Payment Method
   - Account ID
   - Status (Pending/Approved/Rejected/Paid)
   - Created Date

### Step 3: Filter and Search
- **Filter by Status:** Use the filter on the right (Pending, Approved, Rejected, Paid)
- **Filter by Method:** Filter by payment method (eSewa, Khalti, Bank, etc.)
- **Search:** Search by username or account ID

### Step 4: Manage Requests
You can:
- **Approve:** Select requests → Actions → "Approve selected requests"
- **Reject:** Select requests → Actions → "Reject selected requests" (refunds coins)
- **Mark as Paid:** Select requests → Actions → "Mark as paid"
- **Edit:** Click on a request to add admin notes or change status

---

## Method 2: Admin API Endpoints (For Automation)

### List All Withdrawal Requests
```bash
GET https://your-backend.railway.app/api/admin/withdraws/
Authorization: Bearer <admin_token>
```

**Query Parameters:**
- `?status=pending` - Filter by status
- `?method=esewa` - Filter by payment method
- `?status=pending&method=khalti` - Combine filters

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "user": "username",
      "amount_rs": "100.00",
      "method": "esewa",
      "account_id": "98xxxxxxxx",
      "status": "pending",
      "admin_note": "",
      "created_at": "2024-01-15T10:30:00Z",
      "processed_at": null
    }
  ]
}
```

### Get Single Withdrawal Request
```bash
GET https://your-backend.railway.app/api/admin/withdraws/<id>/
Authorization: Bearer <admin_token>
```

### Approve Request
```bash
POST https://your-backend.railway.app/api/admin/withdraws/<id>/approve/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "admin_note": "Approved and processed"
}
```

### Reject Request
```bash
POST https://your-backend.railway.app/api/admin/withdraws/<id>/reject/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "admin_note": "Rejected: Invalid account"
}
```
**Note:** Rejecting automatically refunds coins to user.

### Mark as Paid
```bash
POST https://your-backend.railway.app/api/admin/withdraws/<id>/mark-paid/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "admin_note": "Payment sent via eSewa"
}
```

---

## Method 3: Django Shell (For Advanced Users)

### Access Django Shell
```bash
railway run python manage.py shell
```

### List All Pending Withdrawals
```python
from core.models import WithdrawRequest

# Get all pending withdrawals
pending = WithdrawRequest.objects.filter(status='pending').select_related('user')
for w in pending:
    print(f"{w.user.username}: Rs {w.amount_rs} via {w.method} ({w.account_id})")
```

### Get Statistics
```python
from core.models import WithdrawRequest
from django.db.models import Sum, Count

# Total pending amount
pending_total = WithdrawRequest.objects.filter(
    status='pending'
).aggregate(total=Sum('amount_rs'))['total']

# Count by status
by_status = WithdrawRequest.objects.values('status').annotate(
    count=Count('id')
)

print(f"Pending Total: Rs {pending_total}")
print(by_status)
```

---

## Withdrawal Status Flow

```
Pending → Approved → Paid
   ↓
Rejected (coins refunded)
```

### Status Meanings:
- **Pending:** User submitted request, waiting for admin approval
- **Approved:** Admin approved, ready to process payment
- **Paid:** Payment has been sent to user
- **Rejected:** Request rejected, coins refunded to user

---

## Quick Actions in Admin Panel

### Bulk Approve Pending Requests:
1. Go to Withdraw requests
2. Filter by "Status: Pending"
3. Select all (checkbox at top)
4. Actions → "Approve selected requests"
5. Click "Go"

### Bulk Reject Requests:
1. Select requests
2. Actions → "Reject selected requests"
3. Coins will be automatically refunded

### Add Admin Notes:
1. Click on a withdrawal request
2. Scroll to "Admin Actions"
3. Add note in "Admin note" field
4. Save

---

## Tips

1. **Check Daily:** Review pending withdrawals daily
2. **Verify Account:** Always verify account ID matches user's registered info
3. **Add Notes:** Add admin notes for tracking (e.g., "Payment sent on 2024-01-15")
4. **Filter by Date:** Use admin filters to see recent requests
5. **Export:** Use admin export feature to download CSV of withdrawals

---

## Security Notes

- Admin API endpoints require `IsAdminUser` permission
- Only staff/superuser accounts can access
- Always verify user identity before approving
- Keep admin notes for audit trail

---

## Need Help?

If you can't access admin panel:
1. Create superuser: `railway run python manage.py createsuperuser`
2. Check if user has `is_staff=True` and `is_superuser=True`
3. Verify admin URL is correct: `/admin/`

