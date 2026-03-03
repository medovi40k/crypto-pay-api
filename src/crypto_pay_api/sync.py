from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, Literal

import requests
from requests import Response

from .config import CryptoPayConfig
from .errors import CryptoPayHTTPError
from ._core import resolve_root, clean_params, parse_api_response


class CryptoPay:
    """
    Sync client for Crypto Pay API.
    """

    def __init__(self, config: CryptoPayConfig, *, session: Optional[requests.Session] = None):
        self.config = config
        self._session_external = session is not None
        self._session = session or requests.Session()

        self._root = resolve_root(config)
        self._session.headers.update(
            {
                "Crypto-Pay-API-Token": self.config.token,
                "User-Agent": self.config.user_agent,
            }
        )

    def close(self) -> None:
        if not self._session_external:
            self._session.close()

    def __enter__(self) -> "CryptoPay":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _raise_for_http(self, resp: Response) -> None:
        if resp.status_code >= 400:
            raise CryptoPayHTTPError(f"HTTP {resp.status_code}: {resp.text}")

    def _request(self, method_name: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self._root}/api/{method_name}"
        payload = clean_params(params)
        try:
            if payload:
                resp = self._session.post(url, json=payload, timeout=self.config.timeout)
            else:
                resp = self._session.get(url, timeout=self.config.timeout)
        except requests.RequestException as e:
            raise CryptoPayHTTPError(str(e)) from e

        self._raise_for_http(resp)
        return parse_api_response(resp.json())

    # -------- API methods --------

    def get_me(self) -> Dict[str, Any]:
        return self._request("getMe")

    def create_invoice(
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
        return self._request(
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

    def delete_invoice(self, invoice_id: int) -> bool:
        return self._request("deleteInvoice", {"invoice_id": invoice_id})

    def get_invoices(
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
        return self._request(
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

    def create_check(
        self,
        *,
        asset: str,
        amount: Union[str, float],
        pin_to_user_id: Optional[int] = None,
        pin_to_username: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._request(
            "createCheck",
            {
                "asset": asset,
                "amount": str(amount),
                "pin_to_user_id": pin_to_user_id,
                "pin_to_username": pin_to_username,
            },
        )

    def delete_check(self, check_id: int) -> bool:
        return self._request("deleteCheck", {"check_id": check_id})

    def get_checks(
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
        return self._request(
            "getChecks",
            {
                "asset": asset,
                "check_ids": check_ids,
                "status": status,
                "offset": offset,
                "count": count,
            },
        )

    def transfer(
        self,
        *,
        user_id: int,
        asset: str,
        amount: Union[str, float],
        spend_id: str,
        comment: Optional[str] = None,
        disable_send_notification: Optional[bool] = None,
    ) -> Dict[str, Any]:
        return self._request(
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

    def get_transfers(
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
        return self._request(
            "getTransfers",
            {
                "asset": asset,
                "transfer_ids": transfer_ids,
                "spend_id": spend_id,
                "offset": offset,
                "count": count,
            },
        )

    def get_balance(self) -> List[Dict[str, Any]]:
        return self._request("getBalance")

    def get_exchange_rates(self) -> List[Dict[str, Any]]:
        return self._request("getExchangeRates")

    def get_currencies(self) -> Dict[str, Any]:
        return self._request("getCurrencies")

    def get_stats(self, *, start_at: Optional[str] = None, end_at: Optional[str] = None) -> Dict[str, Any]:
        return self._request("getStats", {"start_at": start_at, "end_at": end_at})