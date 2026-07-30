"""API client for saint of the day providers."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientError, ClientSession

from .const import PROVIDER_FETE_DU_JOUR, PROVIDER_NOMINIS

_LOGGER = logging.getLogger(__name__)

NOMINIS_URL = "https://nominis.cef.fr/json/saintdujour.php"
FETE_DU_JOUR_IP_URL = "http://checkip.dyndns.org"
FETE_DU_JOUR_KEY_URL = "https://fetedujour.fr/api/"
FETE_DU_JOUR_DATA_URL = "https://fetedujour.fr/api/v2/{api_key}/json"

_IP_PATTERN = re.compile(r"([0-9]+(?:\.[0-9]+){3})")
_KEY_PATTERN = re.compile(r"Voici votre clé\s*:.*?>\s*([A-Za-z0-9]+)\s*<", re.DOTALL)

FAKE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


@dataclass(slots=True)
class SaintData:
    """Provider data for one saint of the day."""

    name: str
    source: str
    description: str | None = None
    link: str | None = None
    day: int | None = None
    month: int | None = None
    year: int | None = None


class DailySaintApi:
    """Fetch saint of the day data from supported providers."""

    def __init__(self, session: ClientSession) -> None:
        self._session = session
        self._fete_du_jour_key: str | None = None

    async def async_fetch(self, provider: str) -> SaintData:
        """Fetch data for a provider."""
        if provider == PROVIDER_NOMINIS:
            return await self._async_fetch_nominis()
        if provider == PROVIDER_FETE_DU_JOUR:
            return await self._async_fetch_fete_du_jour()
        msg = f"Unsupported provider: {provider}"
        raise ValueError(msg)

    async def _async_fetch_nominis(self) -> SaintData:
        """Fetch the saint from Nominis."""
        async with self._session.get(NOMINIS_URL) as response:
            response.raise_for_status()
            payload: dict[str, Any] = await response.json()

        root = payload.get("response", {})
        query = root.get("query", {})
        saint = root.get("saintdujour", {})

        name = saint.get("nom")
        if not isinstance(name, str) or not name:
            raise ValueError("Nominis response did not contain a valid saint name")

        return SaintData(
            name=name,
            source=PROVIDER_NOMINIS,
            description=saint.get("description"),
            link=saint.get("lien"),
            day=_safe_int(query.get("jour")),
            month=_safe_int(query.get("mois")),
            year=_safe_int(query.get("annee")),
        )

    async def _async_fetch_fete_du_jour(self) -> SaintData:
        """Fetch the saint from Fête du jour."""
        api_key = await self._async_get_fete_du_jour_key(force_refresh=False)
        try:
            return await self._async_fetch_fete_du_jour_data(api_key)
        except (ClientError, ValueError):
            _LOGGER.debug("Unable to use cached Fête du jour API key, refreshing key")

        api_key = await self._async_get_fete_du_jour_key(force_refresh=True)
        return await self._async_fetch_fete_du_jour_data(api_key)

    async def _async_fetch_fete_du_jour_data(self, api_key: str) -> SaintData:
        """Fetch saint data from Fête du jour using an API key."""
        url = FETE_DU_JOUR_DATA_URL.format(api_key=api_key)
        async with self._session.get(url, headers=FAKE_HEADERS) as response:
            response.raise_for_status()
            payload: dict[str, Any] = await response.json()

        name = payload.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("Fête du jour response did not contain a valid saint name")

        return SaintData(
            name=name,
            source=PROVIDER_FETE_DU_JOUR,
            day=_safe_int(payload.get("day")),
            month=_safe_int(payload.get("month")),
        )

    async def _async_get_fete_du_jour_key(self, force_refresh: bool) -> str:
        """Return a valid Fête du jour API key."""
        if self._fete_du_jour_key and not force_refresh:
            return self._fete_du_jour_key

        async with self._session.get(FETE_DU_JOUR_IP_URL) as response:
            response.raise_for_status()
            ip_content = await response.text()

        ip_match = _IP_PATTERN.search(ip_content)
        if ip_match is None:
            raise ValueError("Unable to extract public IP for Fête du jour key request")

        async with self._session.post(
            FETE_DU_JOUR_KEY_URL, data={"ip": ip_match.group(1)}, headers=FAKE_HEADERS
        ) as response:
            response.raise_for_status()
            key_content = await response.text()

        key_match = _KEY_PATTERN.search(key_content)
        if key_match is None:
            raise ValueError("Unable to extract Fête du jour API key from response")

        self._fete_du_jour_key = key_match.group(1)
        return self._fete_du_jour_key


def _safe_int(value: Any) -> int | None:
    """Convert a value to int if possible."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
