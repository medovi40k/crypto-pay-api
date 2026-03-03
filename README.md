# cryptopay-python-sdk

[![PyPI](https://img.shields.io/pypi/v/cryptopay-python-sdk)](https://pypi.org/project/cryptopay-python-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/cryptopay-python-sdk)](https://pypi.org/project/cryptopay-python-sdk/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Sync + async Python client for the [Telegram Crypto Pay API](https://help.send.tg/en/articles/10279948-crypto-pay-api).

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

## Configuration

```python
CryptoPayConfig(
    token="YOUR_TOKEN",
    network="mainnet",       # or "testnet"
    timeout=20.0,
    base_url_override=None,  # override API base URL if needed
)
```

## Methods

| Method | Description |
|---|---|
| `get_me()` | App info |
| `create_invoice(...)` | Create a payment invoice |
| `delete_invoice(invoice_id)` | Delete invoice |
| `get_invoices(...)` | List invoices |
| `create_check(...)` | Create a check |
| `delete_check(check_id)` | Delete check |
| `get_checks(...)` | List checks |
| `transfer(...)` | Send coins to a Telegram user |
| `get_transfers(...)` | List transfers |
| `get_balance()` | App balance |
| `get_exchange_rates()` | Current exchange rates |
| `get_currencies()` | Supported currencies |
| `get_stats(...)` | App statistics |

## Webhook verification

```python
from crypto_pay_api import verify_webhook_signature

ok = verify_webhook_signature(
    token="YOUR_TOKEN",
    raw_body=request.body,          # raw bytes
    signature_header=request.headers["crypto-pay-api-signature"],
)
```

## Error handling

```python
from crypto_pay_api import CryptoPayAPIError, CryptoPayHTTPError

try:
    invoice = cp.create_invoice(asset="USDT", amount=5)
except CryptoPayAPIError as e:
    print(e.error_code, e.raw)   # API-level error (ok=false)
except CryptoPayHTTPError as e:
    print(e)                     # network / HTTP error
```

## License

MIT
