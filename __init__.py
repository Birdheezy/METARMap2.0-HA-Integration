import logging
import requests  # Ensure requests is imported
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up the METAR Map LED Switch entity."""
    pi_ip = hass.data[DOMAIN][config_entry.entry_id]["pi_ip"]
    name = hass.data[DOMAIN][config_entry.entry_id]["name"]
    async_add_entities([METARMapLEDSwitch(pi_ip, name)])


class METARMapLEDSwitch(SwitchEntity):
    """Switch to control the METAR Map LED."""

    def __init__(self, pi_ip, name):
        self._pi_ip = pi_ip
        self._attr_name = f"{name} LED Switch"
        self._attr_unique_id = f"{name.lower().replace(' ', '_')}_led_switch"
        self._attr_is_on = False  # Default state

    async def async_added_to_hass(self):
        """Run after entity has been added to HA."""
        await self.hass.async_add_executor_job(self.update_status)

    def update_status(self):
        """Fetch the LED status from the Raspberry Pi."""
        url = f"{self._pi_ip}/leds/status"
        try:
            response = requests.get(url, verify=False, timeout=10)
            response.raise_for_status()
            data = response.json()
            self._attr_is_on = data["status"] == "on"
            _LOGGER.debug(f"LED status fetched successfully: {self._attr_is_on}")
        except requests.RequestException as err:
            _LOGGER.error(f"Failed to fetch LED status for {self._attr_name}: {err}")
            self._attr_is_on = False

        # Schedule an update in Home Assistant
        self.schedule_update_ha_state()

    async def async_update(self):
        """Fetch the latest LED status periodically."""
        await self.hass.async_add_executor_job(self.update_status)

    def turn_on(self, **kwargs):
        """Turn on the LEDs."""
        url = f"{self._pi_ip}/leds/on"
        try:
            response = requests.post(url, verify=False, timeout=10)
            response.raise_for_status()
            self._attr_is_on = True
            _LOGGER.debug(f"LEDs turned on successfully for {self._attr_name}")
            self.schedule_update_ha_state()
        except requests.RequestException as err:
            _LOGGER.error(f"Failed to turn on LEDs for {self._attr_name}: {err}")

    def turn_off(self, **kwargs):
        """Turn off the LEDs."""
        url = f"{self._pi_ip}/leds/off"
        try:
            response = requests.post(url, verify=False, timeout=10)
            response.raise_for_status()
            self._attr_is_on = False
            _LOGGER.debug(f"LEDs turned off successfully for {self._attr_name}")
            self.schedule_update_ha_state()
        except requests.RequestException as err:
            _LOGGER.error(f"Failed to turn off LEDs for {self._attr_name}: {err}")
