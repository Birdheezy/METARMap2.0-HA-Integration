"""Sensor platform for METAR Map."""
import logging
import os
import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up the METAR Map Weather Update sensor."""
    name = hass.data[DOMAIN][entry.entry_id]["name"]
    async_add_entities([METARMapWeatherUpdateSensor(name)])

class METARMapWeatherUpdateSensor(SensorEntity):
    """Sensor that tracks when weather was last updated."""

    def __init__(self, name):
        """Initialize the sensor."""
        self._attr_name = f"{name} Last Weather Update"
        self._attr_unique_id = f"{name.lower().replace(' ', '_')}_last_weather_update"
        self._attr_native_value = None
        self._weather_file_path = '/home/pi/weather.json'  # Path to weather.json

    async def async_update(self):
        """Fetch the latest update time."""
        try:
            last_modified_timestamp = os.path.getmtime(self._weather_file_path)
            self._attr_native_value = datetime.datetime.fromtimestamp(
                last_modified_timestamp
            ).strftime('%Y-%m-%d %H:%M:%S')
        except FileNotFoundError:
            self._attr_native_value = "Weather data not available"
            _LOGGER.warning("Weather data file not found") 