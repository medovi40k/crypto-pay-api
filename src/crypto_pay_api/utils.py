from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any, Union


def verify_webhook_signature(*, token: str, raw_body: Union[bytes, str], signature_header: str) -> bool:
    """
    Verify webhook update signature.

    Rule (from docs): compare header `crypto-pay-api-signature` with HMAC-SHA256(body),
    where key = SHA256(app_token). Body is the *entire raw request body*.
    """
    raw = raw_body.encode("utf-8") if isinstance(raw_body, str) else raw_body
    secret = hashlib.sha256(token.encode("utf-8")).digest()
    digest_hex = hmac.new(secret, raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest_hex, signature_header)


def canonical_json_bytes(obj: Any) -> bytes:
    """
    If your framework lost raw body bytes, serialize deterministically:
    compact JSON without spaces.
    """
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode("utf-8")