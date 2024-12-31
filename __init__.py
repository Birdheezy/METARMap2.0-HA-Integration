import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the METAR Map LED Controller from a config entry."""
    
    _LOGGER.info("Setting up METARMap with IP: %s", entry.data["pi_ip"])

    # Store the IP address globally so other parts of the integration can access it
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "pi_ip": entry.data["pi_ip"],
        "name": entry.data["name"],
    }

    # Set up platforms (switch, button, sensor) using the config entry
    await hass.config_entries.async_forward_entry_setups(
        entry, ["switch", "button", "sensor"]
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    
    _LOGGER.info("Unloading METARMap entry with IP: %s", entry.data["pi_ip"])

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, ["switch", "button", "sensor"]
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
