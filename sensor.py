"""Sensor platform for METAR Map."""
import logging
import datetime
import requests
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, ENDPOINT_WEATHER_STATUS
from homeassistant.helpers.entity import EntityCategory

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
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_native_value = None
        self._pi_ip = pi_ip

    async def async_update(self):
        """Fetch the latest update time."""
        try:
            url = f"{self._pi_ip}{ENDPOINT_WEATHER_STATUS}"
            response = requests.get(url, verify=False, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Convert string timestamp to datetime object
            timestamp_str = data.get("last_updated")
            if timestamp_str and timestamp_str != "Weather data not available":
                try:
                    self._attr_native_value = datetime.datetime.strptime(
                        timestamp_str, 
                        '%Y-%m-%d %H:%M:%S'
                    )
                except ValueError:
                    self._attr_native_value = None
                    _LOGGER.error("Invalid timestamp format received: %s", timestamp_str)
            else:
                self._attr_native_value = None
            
        except requests.RequestException as err:
            self._attr_native_value = None
            _LOGGER.error("Failed to get weather update time: %s", err) 