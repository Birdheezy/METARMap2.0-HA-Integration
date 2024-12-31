"""Sensor platform for METAR Map."""
import logging
import datetime
import aiohttp
import async_timeout
from zoneinfo import ZoneInfo
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
    _LOGGER.debug("Setting up METAR Map Weather sensor with IP: %s", pi_ip)
    async_add_entities([METARMapWeatherUpdateSensor(hass, name, pi_ip)])

class METARMapWeatherUpdateSensor(SensorEntity):
    """Sensor that tracks when weather was last updated."""

    def __init__(self, hass, name, pi_ip):
        """Initialize the sensor."""
        self.hass = hass
        self._attr_name = f"{name} Last Weather Update"
        self._attr_unique_id = f"{name.lower().replace(' ', '_')}_last_weather_update"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_native_value = None
        self._pi_ip = pi_ip
        self._attr_should_poll = True
        self._attr_suggested_update_interval = datetime.timedelta(seconds=30)
        _LOGGER.debug("Initialized weather sensor with IP: %s", self._pi_ip)

    async def async_update(self):
        """Fetch the latest update time."""
        try:
            url = f"{self._pi_ip}{ENDPOINT_WEATHER_STATUS}"
            _LOGGER.debug("Fetching weather update from: %s", url)
            
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, ssl=False) as response:
                        response.raise_for_status()
                        data = await response.json()
                        
            _LOGGER.debug("Received weather data: %s", data)
            
            # Convert string timestamp to datetime object
            timestamp_str = data.get("last_updated")
            _LOGGER.debug("Extracted timestamp: %s", timestamp_str)
            
            if timestamp_str and timestamp_str != "Weather data not available":
                try:
                    # Parse the timestamp and add the system timezone
                    naive_dt = datetime.datetime.strptime(
                        timestamp_str, 
                        '%Y-%m-%d %H:%M:%S'
                    )
                    # Add the timezone from Home Assistant's configuration
                    self._attr_native_value = naive_dt.replace(
                        tzinfo=ZoneInfo(self.hass.config.time_zone)
                    )
                    _LOGGER.debug("Converted timestamp to datetime with timezone: %s", self._attr_native_value)
                except ValueError:
                    self._attr_native_value = None
                    _LOGGER.error("Invalid timestamp format received: %s", timestamp_str)
            else:
                self._attr_native_value = None
                _LOGGER.warning("No valid timestamp received")
            
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            self._attr_native_value = None
            _LOGGER.error("Failed to get weather update time: %s", err) 