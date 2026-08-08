"""Entidade base com device_info compartilhado.
Autor: juniordsj1990-code
Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo, Entity

from .const import DOMAIN
from .coordinator import BotijaoGasData

REPO_URL = "https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant"


class BotijaoGasEntity(Entity):
    """Classe base: agrupa todas as entidades sob um único dispositivo."""

    _attr_has_entity_name = True

    def __init__(
        self, data: BotijaoGasData, entry: ConfigEntry, key: str
    ) -> None:
        self._data = data
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=data.device_name,
            manufacturer="ELETRICA DAN · juniordsj1990-code",
            model="Balança HX711 (via Tasmota)",
            configuration_url=REPO_URL,
        )

    async def async_added_to_hass(self) -> None:
        self._data.add_listener(self._on_update)

    async def async_will_remove_from_hass(self) -> None:
        self._data.remove_listener(self._on_update)

    def _on_update(self) -> None:
        self.async_write_ha_state()
