from __future__ import annotations

from typing import Any, Dict, Optional

from .config import CryptoPayConfig
from .errors import CryptoPayAPIError, CryptoPayHTTPError


def resolve_root(cfg: CryptoPayConfig) -> str:
    if cfg.base_url_override:
        return cfg.base_url_override.rstrip("/")
    return "https://pay.crypt.bot" if cfg.network == "mainnet" else "https://testnet-pay.crypt.bot"


def clean_params(params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not params:
        return {}
    return {k: v for k, v in params.items() if v is not None}


def parse_api_response(data: Any) -> Any:
    if not isinstance(data, dict) or "ok" not in data:
        raise CryptoPayHTTPError(f"Unexpected response: {data!r}")

    if data.get("ok") is True:
        return data.get("result")

    raise CryptoPayAPIError(str(data.get("error", "UNKNOWN_ERROR")), raw=data)