# Coin Value Update to 0.025

## ✅ Changes Made

The coin value has been updated from **Rs. 0.1** to **Rs. 0.025** per coin.

### Files Updated:

1. **`core/management/commands/setup_settings.py`**
   - Updated default `COIN_TO_RS_RATE` from `"0.1"` to `"0.025"`

2. **`core/views.py`**
   - Updated fallback value in `WalletView` from `"0.1"` to `"0.025"`
   - Updated fallback value in `WithdrawRequestView` from `"0.1"` to `"0.025"`

3. **`core/admin.py`**
   - Updated fallback value in `reject_requests` method from `"0.1"` to `"0.025"`

## 📊 Impact

- **Before**: 1 coin = Rs. 0.1
- **After**: 1 coin = Rs. 0.025

### Examples:
- **100 coins** = Rs. 2.50 (was Rs. 10.00)
- **1000 coins** = Rs. 25.00 (was Rs. 100.00)
- **2000 coins** = Rs. 50.00 (was Rs. 200.00) - Minimum withdrawal

## 🔄 Next Steps

1. **Run setup_settings command** on Railway to update the database:
   ```bash
   python manage.py setup_settings
   ```

2. **Verify** the setting is updated in the database:
   - Check admin panel: Settings → COIN_TO_RS_RATE should be "0.025"

3. **Test** withdrawal calculations:
   - Rs. 50 withdrawal now requires 2000 coins (was 500 coins)
   - Wallet balance calculations should reflect new rate

## ⚠️ Note

This change affects:
- Wallet balance display (Rs. equivalent)
- Withdrawal calculations
- All coin-to-rupee conversions throughout the app

The change will take effect immediately after running `setup_settings` command.

