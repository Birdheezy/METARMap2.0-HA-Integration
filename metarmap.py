import logging
import requests
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "metarmap"
_LOGGER = logging.getLogger(__name__)

# URLs for the REST API on the Raspberry Pi
LED_ON_URL = "http://192.168.70.167/leds/on"
LED_OFF_URL = "http://192.168.70.167/leds/off"
WEATHER_UPDATE_URL = "http://192.168.70.167/update-weather"

def setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the METAR Map LED Controller with services only."""

    def handle_turn_on(call):
        """Handle turning on the LEDs."""
        try:
            requests.post(LED_ON_URL)
            _LOGGER.info("METAR Map LEDs turned on successfully")
        except requests.RequestException as err:
            _LOGGER.error(f"Failed to turn on LEDs: {err}")

    def handle_turn_off(call):
        """Handle turning off the LEDs."""
        try:
            requests.post(LED_OFF_URL)
            _LOGGER.info("METAR Map LEDs turned off successfully")
        except requests.RequestException as err:
            _LOGGER.error(f"Failed to turn off LEDs: {err}")

    def handle_update_weather(call):
        """Handle updating the weather."""
        try:
            requests.post(WEATHER_UPDATE_URL)
            _LOGGER.info("Weather updated successfully")
        except requests.RequestException as err:
            _LOGGER.error(f"Failed to update weather: {err}")

    # Register the on, off, and update weather services directly
    hass.services.register(DOMAIN, "turn_on", handle_turn_on)
    hass.services.register(DOMAIN, "turn_off", handle_turn_off)
    hass.services.register(DOMAIN, "update_weather", handle_update_weather)

    _LOGGER.info("METAR Map integration set up with services successfully")
    return True
