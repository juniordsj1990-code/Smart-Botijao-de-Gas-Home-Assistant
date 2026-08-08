"""Binary sensor de alerta de gás baixo.
Autor: juniordsj1990-code
Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
"""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_COORDINATOR, DOMAIN, KEY_GAS_BAIXO
from .coordinator import BotijaoGasData
from .entity import BotijaoGasEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    data: BotijaoGasData = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    async_add_entities([GasBaixoBinarySensor(data, entry)])


class GasBaixoBinarySensor(BotijaoGasEntity, BinarySensorEntity):
    """Liga quando o peso disponível fica abaixo do limite de alerta.
    Equivalente ao antigo sensor.botijao_de_gas_esgotamento_template."""

    _attr_translation_key = "gas_baixo"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:gas-cylinder"

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_GAS_BAIXO)

    @property
    def is_on(self) -> bool:
        return self._data.gas_baixo
