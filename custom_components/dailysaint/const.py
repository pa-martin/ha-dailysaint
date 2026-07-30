"""Constants for the Daily Saint integration."""

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "dailysaint"
PLATFORMS: list[Platform] = [Platform.SENSOR]

CONF_PROVIDERS = "providers"

PROVIDER_NOMINIS = "nominis"
PROVIDER_FETE_DU_JOUR = "fetedujour"

PROVIDER_NAMES: dict[str, str] = {
    PROVIDER_NOMINIS: "Nominis",
    PROVIDER_FETE_DU_JOUR: "Fête du jour",
}

DEFAULT_PROVIDERS: list[str] = [PROVIDER_NOMINIS, PROVIDER_FETE_DU_JOUR]
UPDATE_INTERVAL = timedelta(hours=6)
