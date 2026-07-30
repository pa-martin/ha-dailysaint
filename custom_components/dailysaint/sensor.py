"""Sensor platform for Daily Saint."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import DailySaintCoordinator
from .const import CONF_PROVIDERS, DEFAULT_PROVIDERS, DOMAIN, PROVIDER_NAMES


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Daily Saint sensors based on config entry."""
    coordinator: DailySaintCoordinator = entry.runtime_data
    providers = entry.options.get(CONF_PROVIDERS, entry.data.get(CONF_PROVIDERS, DEFAULT_PROVIDERS))
    async_add_entities([DailySaintSensor(coordinator, entry, provider) for provider in providers])


class DailySaintSensor(CoordinatorEntity[DailySaintCoordinator], SensorEntity):
    """Representation of one provider saint sensor."""

    _attr_has_entity_name = True
    _attr_translation_key = "saint_of_the_day"
    _attr_icon = "mdi:cross"

    def __init__(self, coordinator: DailySaintCoordinator, entry: ConfigEntry, provider: str) -> None:
        """Initialize sensor entity."""
        super().__init__(coordinator)
        self._provider = provider
        self._provider_name = PROVIDER_NAMES.get(provider, provider)
        self._attr_unique_id = f"{entry.entry_id}_{provider}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, provider)},
            name=f"Daily Saint {self._provider_name}",
            manufacturer=self._provider_name,
            model="Saint of the day",
        )
        self._attr_name = self._provider_name

    @property
    def available(self) -> bool:
        """Return whether entity is available."""
        return super().available and self._provider in self.coordinator.data

    @property
    def native_value(self) -> str | None:
        """Return current saint name."""
        provider_data = self.coordinator.data.get(self._provider)
        if provider_data is None:
            return None
        return provider_data.name

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra entity attributes."""
        provider_data = self.coordinator.data.get(self._provider)
        if provider_data is None:
            return {}

        attrs: dict[str, Any] = {
            ATTR_ATTRIBUTION: self._provider_name,
            "provider": self._provider,
            "description": provider_data.description,
            "link": provider_data.link,
            "day": provider_data.day,
            "month": provider_data.month,
            "year": provider_data.year,
        }
        return {key: value for key, value in attrs.items() if value is not None}
