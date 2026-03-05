import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components.network import async_get_source_ip
from .const import DOMAIN, CONF_LISTEN_IP


class TendaBeliConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="Tenda Beli", data=user_input)

        auto_ip = await async_get_source_ip(self.hass)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional(CONF_LISTEN_IP, default=auto_ip): str,
            }),
        )
