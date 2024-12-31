"""Sensor platform for METAR Map."""
import logging
import datetime
import requests
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, ENDPOINT_WEATHER_STATUS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up the METAR Map Weather Update sensor."""
    name = hass.data[DOMAIN][entry.entry_id]["name"]
    pi_ip = hass.data[DOMAIN][entry.entry_id]["pi_ip"]
    async_add_entities([METARMapWeatherUpdateSensor(name, pi_ip)])

class METARMapWeatherUpdateSensor(SensorEntity):
    """Sensor that tracks when weather was last updated."""

    def __init__(self, name, pi_ip):
        """Initialize the sensor."""
        self._attr_name = f"{name} Last Weather Update"
        self._attr_unique_id = f"{name.lower().replace(' ', '_')}_last_weather_update"
        self._attr_native_value = None
        self._pi_ip = pi_ip

    async def async_update(self):
        """Fetch the latest update time."""
        try:
            url = f"{self._pi_ip}{ENDPOINT_WEATHER_STATUS}"
            response = requests.get(url, verify=False, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Assuming the API returns a timestamp
            self._attr_native_value = data.get("last_updated", "Weather data not available")
            
        except requests.RequestException as err:
            self._attr_native_value = "Connection error"
            _LOGGER.error("Failed to get weather update time: %s", err) 