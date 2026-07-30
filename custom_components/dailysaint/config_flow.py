"""Config flow for Daily Saint integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import CONF_PROVIDERS, DEFAULT_PROVIDERS, DOMAIN, PROVIDER_NAMES


def _providers_schema(current: list[str] | None = None) -> vol.Schema:
    """Return providers selection schema."""
    return vol.Schema(
        {
            vol.Required(
                CONF_PROVIDERS, default=current or DEFAULT_PROVIDERS
            ): SelectSelector(
                SelectSelectorConfig(
                    options=[
                        SelectOptionDict(value=provider, label=label)
                        for provider, label in PROVIDER_NAMES.items()
                    ],
                    mode=SelectSelectorMode.DROPDOWN,
                    multiple=True,
                )
            )
        }
    )


class DailySaintConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle config flow for Daily Saint."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, list[str]] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors: dict[str, str] = {}
        if user_input is not None:
            providers = user_input.get(CONF_PROVIDERS, [])
            if providers:
                return self.async_create_entry(
                    title="Daily Saint", data={}, options=user_input
                )
            errors["base"] = "no_provider"

        return self.async_show_form(
            step_id="user", data_schema=_providers_schema(), errors=errors
        )

    @staticmethod
    def async_get_options_flow(_config_entry) -> OptionsFlow:
        """Return options flow."""
        return DailySaintOptionsFlow()


class DailySaintOptionsFlow(OptionsFlow):
    """Handle options flow for Daily Saint."""

    async def async_step_init(
        self, user_input: dict[str, list[str]] | None = None
    ) -> ConfigFlowResult:
        """Manage integration options."""
        errors: dict[str, str] = {}
        if user_input is not None:
            providers = user_input.get(CONF_PROVIDERS, [])
            if providers:
                # Removes providers which are unselected
                device_registry = dr.async_get(self.hass)
                for provider in self.config_entry.options.get(CONF_PROVIDERS, []):
                    # We firstly get the right device
                    device = device_registry.async_get_device(
                        identifiers={(DOMAIN, provider)}
                    )
                    if device and provider not in providers:
                        # And then, we remove it thanks to its id
                        device_registry.async_update_device(
                            device_id=device.id,
                            remove_config_entry_id=self.config_entry.entry_id,
                        )

                return self.async_create_entry(title="", data=user_input)
            errors["base"] = "no_provider"

        return self.async_show_form(
            step_id="init",
            data_schema=_providers_schema(
                list(self.config_entry.options.get(CONF_PROVIDERS, DEFAULT_PROVIDERS))
            ),
            errors=errors,
        )
