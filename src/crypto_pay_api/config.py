from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional


MainnetOrTestnet = Literal["mainnet", "testnet"]


@dataclass(frozen=True)
class CryptoPayConfig:
    token: str
    network: MainnetOrTestnet = "mainnet"
    timeout: float = 20.0
    base_url_override: Optional[str] = None  # e.g. "https://pay.crypt.bot"
    user_agent: str = "crypto-pay-api/0.1.3"