from __future__ import annotations

import logging
from homeassistant.core import HomeAssistant, Context
from homeassistant.components.network import async_get_source_ip
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, HUB, CONF_LISTEN_IP
from .tenda import TendaBeliServer

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ['switch', 'sensor']

async def async_setup(hass: HomeAssistant, config) -> bool:
    if config.get(DOMAIN) is not None:
        hass.data[DOMAIN] = {}
        hub = TendaBeli(hass)
        await hub.start()
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, hub.stop)

        for platform in PLATFORMS:
            _LOGGER.debug(f"Starting {platform} platform")
            hass.async_create_task(async_load_platform(hass, platform, DOMAIN, None, config))

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    listen_ip = entry.data.get(CONF_LISTEN_IP) or None
    tb = TendaBeli(hass)
    await tb.start(listen_ip)
    hass.data[DOMAIN]["_instance"] = tb
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        tb: TendaBeli = hass.data[DOMAIN].pop("_instance", None)
        if tb:
            tb.stop()
        hass.data.pop(DOMAIN, None)
    return unload_ok


class TendaBeli:
    def __init__(self, hass):
        self.hass = hass
        self.hub = hass.data[DOMAIN][HUB] = TendaBeliServer()
        self.context = Context()

    async def start(self, listen_ip: str | None = None):
        haip: str = listen_ip or await async_get_source_ip(self.hass)
        await self.hub.listen(haip)

    def stop(self, event=None):
        self.hub.stop()
