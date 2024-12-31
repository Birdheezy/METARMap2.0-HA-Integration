import logging
import requests
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the METAR Map LED Controller with services only."""
    
    # Get the pi_ip from the first config entry (if any exist)
    entries = hass.config_entries.async_entries(DOMAIN)
    if not entries:
        _LOGGER.error("No config entries found for METAR Map")
        return False
        
    pi_ip = entries[0].data["pi_ip"]
    
    # Define URLs using the pi_ip
    led_on_url = f"{pi_ip}/leds/on"
    led_off_url = f"{pi_ip}/leds/off"
    weather_update_url = f"{pi_ip}/update-weather"

    def handle_turn_on(call):
        """Handle turning on the LEDs."""
        try:
            requests.post(led_on_url)
            _LOGGER.info("METAR Map LEDs turned on successfully")
        except requests.RequestException as err:
            _LOGGER.error(f"Failed to turn on LEDs: {err}")

    def handle_turn_off(call):
        """Handle turning off the LEDs."""
        try:
            requests.post(led_off_url)
            _LOGGER.info("METAR Map LEDs turned off successfully")
        except requests.RequestException as err:
            _LOGGER.error(f"Failed to turn off LEDs: {err}")

    def handle_update_weather(call):
        """Handle updating the weather."""
        try:
            requests.post(weather_update_url)
            _LOGGER.info("Weather updated successfully")
        except requests.RequestException as err:
            _LOGGER.error(f"Failed to update weather: {err}")

    # Register the on, off, and update weather services directly
    hass.services.register(DOMAIN, "turn_on", handle_turn_on)
    hass.services.register(DOMAIN, "turn_off", handle_turn_off)
    hass.services.register(DOMAIN, "update_weather", handle_update_weather)

    _LOGGER.info("METAR Map integration set up with services successfully")
    return True
