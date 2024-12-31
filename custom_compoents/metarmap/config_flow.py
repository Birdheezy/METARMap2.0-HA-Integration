from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from .const import DOMAIN
from homeassistant.core import HomeAssistant

class METARMapConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for METAR Map LED Controller."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the IP address (basic validation with protocol)
            pi_ip = user_input.get("pi_ip", "").strip()
            if not (pi_ip.startswith("http://") or pi_ip.startswith("https://")):
                errors["pi_ip"] = "invalid_url"  # Add error for invalid URL
            else:
                # Save the data and create the config entry
                return self.async_create_entry(
                    title=user_input["name"],  # Use the custom name as the title
                    data={
                        "pi_ip": pi_ip,
                        "name": user_input["name"],
                    },
                )

        # Display the form
        data_schema = vol.Schema(
            {
                vol.Required("pi_ip", default="http://"): str,
                vol.Required("name", default="METAR Map"): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for METAR Map integration."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Define options schema
        options_schema = vol.Schema(
            {
                vol.Required("pi_ip", default=self.config_entry.data.get("pi_ip", "http://")): str,
                vol.Required("name", default=self.config_entry.data.get("name", "METAR Map")): str,
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
