# cryptopay-python-sdk

[![PyPI](https://img.shields.io/pypi/v/cryptopay-python-sdk)](https://pypi.org/project/cryptopay-python-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/cryptopay-python-sdk)](https://pypi.org/project/cryptopay-python-sdk/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Sync + async Python client for the [Telegram Crypto Pay API](https://help.send.tg/en/articles/10279948-crypto-pay-api).

Supports Python 3.9+, type-annotated, and has no heavy dependencies — just `httpx` for async and `requests` for sync.

## Install

```bash
pip install cryptopay-python-sdk
```

## Quick start

**Async** (recommended)

```python
import asyncio
from crypto_pay_api import CryptoPayAsync, CryptoPayConfig

async def main():
    cfg = CryptoPayConfig(token="YOUR_TOKEN")
    async with CryptoPayAsync(cfg) as cp:
        invoice = await cp.create_invoice(asset="USDT", amount=5)
        print(invoice["pay_url"])

asyncio.run(main())
```

**Sync**

```python
from crypto_pay_api import CryptoPay, CryptoPayConfig

cfg = CryptoPayConfig(token="YOUR_TOKEN")
with CryptoPay(cfg) as cp:
    invoice = cp.create_invoice(asset="USDT", amount=5)
    print(invoice["pay_url"])
```

Both clients are context managers that close the underlying HTTP session automatically.

## Configuration

```python
from crypto_pay_api import CryptoPayConfig

cfg = CryptoPayConfig(
    token="YOUR_TOKEN",          # required — get it from @CryptoBot on Telegram
    network="mainnet",           # "mainnet" (default) or "testnet"
    timeout=20.0,                # request timeout in seconds (default: 20.0)
    base_url_override=None,      # override the API base URL if needed
)
```

## Methods

All methods are available on both `CryptoPay` (sync) and `CryptoPayAsync` (async) with identical signatures.

### App

| Method | Description |
|---|---|
| `get_me()` | Returns basic info about the app associated with the token |
| `get_balance()` | Returns list of balance objects per asset |
| `get_exchange_rates()` | Returns current exchange rates |
| `get_currencies()` | Returns list of supported currencies |
| `get_stats(*, start_at, end_at)` | Returns app statistics for a given date range |

### Invoices

| Method | Description |
|---|---|
| `create_invoice(*, amount, ...)` | Create a payment invoice |
| `delete_invoice(invoice_id)` | Delete an invoice by ID |
| `get_invoices(*, asset, fiat, invoice_ids, status, offset, count)` | List invoices with optional filters |

**`create_invoice` parameters:**

| Parameter | Type | Description |
|---|---|---|
| `amount` | `str \| float` | Amount to charge (required) |
| `currency_type` | `"crypto" \| "fiat"` | Type of currency (optional) |
| `asset` | `str` | Crypto asset, e.g. `"USDT"`, `"TON"` |
| `fiat` | `str` | Fiat currency code, e.g. `"USD"` |
| `accepted_assets` | `str` | Comma-separated accepted assets (for fiat invoices) |
| `swap_to` | `str` | Auto-swap received asset to this asset |
| `description` | `str` | Invoice description shown to the payer |
| `hidden_message` | `str` | Message shown after payment |
| `paid_btn_name` | `str` | Label for the button after payment |
| `paid_btn_url` | `str` | URL for the button after payment |
| `payload` | `str` | Custom string attached to the invoice (max 4kb) |
| `allow_comments` | `bool` | Allow payer to leave a comment |
| `allow_anonymous` | `bool` | Allow anonymous payments |
| `expires_in` | `int` | Invoice lifetime in seconds |

### Checks

| Method | Description |
|---|---|
| `create_check(*, asset, amount, pin_to_user_id, pin_to_username)` | Create a check |
| `delete_check(check_id)` | Delete a check by ID |
| `get_checks(*, asset, check_ids, status, offset, count)` | List checks with optional filters |

### Transfers

| Method | Description |
|---|---|
| `transfer(*, user_id, asset, amount, spend_id, comment, disable_send_notification)` | Send coins to a Telegram user |
| `get_transfers(*, asset, transfer_ids, spend_id, offset, count)` | List transfers with optional filters |

## Webhook verification

Verify incoming webhooks from Crypto Pay using the built-in helper:

```python
from crypto_pay_api import verify_webhook_signature

is_valid = verify_webhook_signature(
    token="YOUR_TOKEN",
    raw_body=request.body,                                    # raw bytes
    signature_header=request.headers["crypto-pay-api-signature"],
)

if not is_valid:
    return 403
```

## Error handling

```python
from crypto_pay_api import CryptoPayAPIError, CryptoPayHTTPError

try:
    invoice = cp.create_invoice(asset="USDT", amount=5)
except CryptoPayAPIError as e:
    # API returned ok=false (e.g. invalid token, bad params)
    print(e.error_code)  # string error code from the API
    print(e.raw)         # full raw response dict
except CryptoPayHTTPError as e:
    # Network error or non-2xx HTTP response
    print(e)
```

**Error hierarchy:**

```
CryptoPayError          ← base class
├── CryptoPayAPIError   ← API returned ok=false
└── CryptoPayHTTPError  ← network / HTTP-level error
```

## License

MIT
