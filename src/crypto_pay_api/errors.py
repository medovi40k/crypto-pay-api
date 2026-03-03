from __future__ import annotations
from typing import Any, Dict, Optional


class CryptoPayError(Exception):
    """Base error for Crypto Pay clients."""


class CryptoPayAPIError(CryptoPayError):
    """Raised when API returns ok=false."""

    def __init__(self, error_code: str, raw: Optional[Dict[str, Any]] = None):
        super().__init__(error_code)
        self.error_code = error_code
        self.raw = raw or {}


class CryptoPayHTTPError(CryptoPayError):
    """Raised on network / HTTP errors."""