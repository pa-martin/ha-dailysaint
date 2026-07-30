"""Coordinator for Daily Saint integration."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import DailySaintApi, SaintData
from .const import CONF_PROVIDERS, DEFAULT_PROVIDERS, DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class DailySaintCoordinator(DataUpdateCoordinator[dict[str, SaintData]]):
    """Handle polling and provider aggregation."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self._api = DailySaintApi(async_get_clientsession(hass))

    @property
    def providers(self) -> list[str]:
        """Return configured providers."""
        providers = self.config_entry.options.get(
            CONF_PROVIDERS, self.config_entry.data.get(CONF_PROVIDERS, DEFAULT_PROVIDERS)
        )
        return list(providers)

    async def _async_update_data(self) -> dict[str, SaintData]:
        """Fetch data from all configured providers."""
        providers = self.providers
        tasks = [self._api.async_fetch(provider) for provider in providers]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        data: dict[str, SaintData] = {}
        for provider, result in zip(providers, results, strict=True):
            if isinstance(result, Exception):
                _LOGGER.warning("Unable to update provider %s: %s", provider, result)
                continue
            data[provider] = result

        if not data:
            raise UpdateFailed("Unable to update any Daily Saint provider")

        return data
