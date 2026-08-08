"""Integração Botijão de Gás para Home Assistant.
Autor: juniordsj1990-code
Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DATA_COORDINATOR, DOMAIN
from .coordinator import BotijaoGasData

PLATFORMS: list[str] = ["sensor", "binary_sensor", "number", "button", "datetime"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configura a integração a partir de uma config entry."""
    data = BotijaoGasData(hass, entry)
    data.async_setup()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {DATA_COORDINATOR: data}

    entry.async_on_unload(entry.add_update_listener(_async_update_options))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Remove a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        data = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
        data.async_unload()
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def _async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Recarrega a integração quando as opções mudam (fator de escala, filtro)."""
    await hass.config_entries.async_reload(entry.entry_id)
