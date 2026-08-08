"""Entidade datetime: data/hora da última troca do botijão.
Autor: juniordsj1990-code
Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
"""
from __future__ import annotations

from datetime import datetime

from homeassistant.components.datetime import DateTimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_COORDINATOR, DOMAIN, KEY_ULTIMA_TROCA
from .coordinator import BotijaoGasData
from .entity import BotijaoGasEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    data: BotijaoGasData = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    async_add_entities([UltimaTrocaDateTime(data, entry)])


class UltimaTrocaDateTime(BotijaoGasEntity, DateTimeEntity, RestoreEntity):
    """Data/hora da última troca do botijão. Equivalente ao antigo
    input_datetime.ultima_troca_do_gas. É usada por Dias em Uso e pela
    Estimativa de Esgotamento."""

    _attr_translation_key = "ultima_troca"
    _attr_icon = "mdi:calendar-refresh"

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_ULTIMA_TROCA)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state is not None and last_state.state not in (
            None,
            "unknown",
            "unavailable",
        ):
            try:
                self._data.ultima_troca = datetime.fromisoformat(last_state.state)
            except ValueError:
                self._data.ultima_troca = None
        self._data.recompute_from_params()

    @property
    def native_value(self) -> datetime | None:
        return self._data.ultima_troca

    async def async_set_value(self, value: datetime) -> None:
        self._data.ultima_troca = value
        self._data.recompute_from_params()
        self.async_write_ha_state()
