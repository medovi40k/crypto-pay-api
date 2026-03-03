from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, Literal

import httpx

from .config import CryptoPayConfig
from .errors import CryptoPayHTTPError
from ._core import resolve_root, clean_params, parse_api_response


class CryptoPayAsync:
    """
    Async client for Crypto Pay API.
    """

    def __init__(self, config: CryptoPayConfig, *, client: Optional[httpx.AsyncClient] = None):
        self.config = config
        self._client_external = client is not None
        self._client = client
        self._root = resolve_root(config)

    async def __aenter__(self) -> "CryptoPayAsync":
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self._root,
                timeout=self.config.timeout,
                headers={
                    "Crypto-Pay-API-Token": self.config.token,
                    "User-Agent": self.config.user_agent,
                },
            )
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._client and not self._client_external:
            await self._client.aclose()
        self._client = None

    async def _request(self, method_name: str, params: Optional[Dict[str, Any]] = None) -> Any:
        if self._client is None:
            async with self:
                return await self._request(method_name, params=params)

        url = f"/api/{method_name}"
        payload = clean_params(params)

        try:
            if payload:
                resp = await self._client.post(url, json=payload)
            else:
                resp = await self._client.get(url)
        except httpx.HTTPError as e:
            raise CryptoPayHTTPError(str(e)) from e

        if resp.status_code >= 400:
            raise CryptoPayHTTPError(f"HTTP {resp.status_code}: {resp.text}")

        return parse_api_response(resp.json())

    # -------- API methods --------

    async def get_me(self) -> Dict[str, Any]:
        return await self._request("getMe")

    async def create_invoice(
        self,
        *,
        amount: Union[str, float],
        currency_type: Optional[Literal["crypto", "fiat"]] = None,
        asset: Optional[str] = None,
        fiat: Optional[str] = None,
        accepted_assets: Optional[str] = None,
        swap_to: Optional[str] = None,
        description: Optional[str] = None,
        hidden_message: Optional[str] = None,
        paid_btn_name: Optional[str] = None,
        paid_btn_url: Optional[str] = None,
        payload: Optional[str] = None,
        allow_comments: Optional[bool] = None,
        allow_anonymous: Optional[bool] = None,
        expires_in: Optional[int] = None,
    ) -> Dict[str, Any]:
        return await self._request(
            "createInvoice",
            {
                "currency_type": currency_type,
                "asset": asset,
                "fiat": fiat,
                "accepted_assets": accepted_assets,
                "amount": str(amount),
                "swap_to": swap_to,
                "description": description,
                "hidden_message": hidden_message,
                "paid_btn_name": paid_btn_name,
                "paid_btn_url": paid_btn_url,
                "payload": payload,
                "allow_comments": allow_comments,
                "allow_anonymous": allow_anonymous,
                "expires_in": expires_in,
            },
        )

    async def delete_invoice(self, invoice_id: int) -> bool:
        return await self._request("deleteInvoice", {"invoice_id": invoice_id})

    async def get_invoices(
        self,
        *,
        asset: Optional[str] = None,
        fiat: Optional[str] = None,
        invoice_ids: Optional[Union[str, List[int]]] = None,
        status: Optional[Literal["active", "paid"]] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        if isinstance(invoice_ids, list):
            invoice_ids = ",".join(str(i) for i in invoice_ids)
        return await self._request(
            "getInvoices",
            {
                "asset": asset,
                "fiat": fiat,
                "invoice_ids": invoice_ids,
                "status": status,
                "offset": offset,
                "count": count,
            },
        )

    async def create_check(
        self,
        *,
        asset: str,
        amount: Union[str, float],
        pin_to_user_id: Optional[int] = None,
        pin_to_username: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self._request(
            "createCheck",
            {
                "asset": asset,
                "amount": str(amount),
                "pin_to_user_id": pin_to_user_id,
                "pin_to_username": pin_to_username,
            },
        )

    async def delete_check(self, check_id: int) -> bool:
        return await self._request("deleteCheck", {"check_id": check_id})

    async def get_checks(
        self,
        *,
        asset: Optional[str] = None,
        check_ids: Optional[Union[str, List[int]]] = None,
        status: Optional[Literal["active", "activated"]] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        if isinstance(check_ids, list):
            check_ids = ",".join(str(i) for i in check_ids)
        return await self._request(
            "getChecks",
            {
                "asset": asset,
                "check_ids": check_ids,
                "status": status,
                "offset": offset,
                "count": count,
            },
        )

    async def transfer(
        self,
        *,
        user_id: int,
        asset: str,
        amount: Union[str, float],
        spend_id: str,
        comment: Optional[str] = None,
        disable_send_notification: Optional[bool] = None,
    ) -> Dict[str, Any]:
        return await self._request(
            "transfer",
            {
                "user_id": user_id,
                "asset": asset,
                "amount": str(amount),
                "spend_id": spend_id,
                "comment": comment,
                "disable_send_notification": disable_send_notification,
            },
        )

    async def get_transfers(
        self,
        *,
        asset: Optional[str] = None,
        transfer_ids: Optional[Union[str, List[int]]] = None,
        spend_id: Optional[str] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        if isinstance(transfer_ids, list):
            transfer_ids = ",".join(str(i) for i in transfer_ids)
        return await self._request(
            "getTransfers",
            {
                "asset": asset,
                "transfer_ids": transfer_ids,
                "spend_id": spend_id,
                "offset": offset,
                "count": count,
            },
        )

    async def get_balance(self) -> List[Dict[str, Any]]:
        return await self._request("getBalance")

    async def get_exchange_rates(self) -> List[Dict[str, Any]]:
        return await self._request("getExchangeRates")

    async def get_currencies(self) -> Dict[str, Any]:
        return await self._request("getCurrencies")

    async def get_stats(self, *, start_at: Optional[str] = None, end_at: Optional[str] = None) -> Dict[str, Any]:
        return await self._request("getStats", {"start_at": start_at, "end_at": end_at})