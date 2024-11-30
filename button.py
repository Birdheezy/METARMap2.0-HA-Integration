import logging
import requests  # Ensure requests is imported
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up the METAR Map Weather Update Button entity."""
    pi_ip = hass.data[DOMAIN][config_entry.entry_id]["pi_ip"]
    name = hass.data[DOMAIN][config_entry.entry_id]["name"]
    async_add_entities([METARMapWeatherButton(pi_ip, name)])

class METARMapWeatherButton(ButtonEntity):
    """Button to trigger a weather update on the METAR Map."""

    def __init__(self, pi_ip, name):
        self._pi_ip = pi_ip
        self._attr_name = f"{name} Weather Update"
        self._attr_unique_id = f"{name.lower().replace(' ', '_')}_weather_update"

    def press(self):
        """Trigger a weather update by sending a POST request to the Raspberry Pi."""
        url = f"{self._pi_ip}/update-weather"
        try:
            response = requests.post(url, verify=False, timeout=10)
            response.raise_for_status()
            _LOGGER.info(f"Weather update triggered successfully for {self._attr_name}")
        except requests.RequestException as err:
            _LOGGER.error(f"Failed to trigger weather update for {self._attr_name}: {err}")
