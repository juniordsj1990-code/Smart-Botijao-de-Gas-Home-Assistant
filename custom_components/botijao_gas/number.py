"""Entidades number editáveis: tara, ajuste fino, zero da balança e limite de alerta.
Autor: juniordsj1990-code
Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
"""
from __future__ import annotations

from homeassistant.components.number import NumberMode, RestoreNumber
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfMass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    AJUSTE_MAX,
    AJUSTE_MIN,
    ALERT_THRESHOLD_MAX,
    ALERT_THRESHOLD_MIN,
    DATA_COORDINATOR,
    DEFAULT_AJUSTE,
    DEFAULT_ALERT_THRESHOLD,
    DEFAULT_RAW_ZERO_OFFSET,
    DEFAULT_TARA,
    DOMAIN,
    KEY_AJUSTE,
    KEY_LIMITE_ALERTA,
    KEY_TARA,
    KEY_ZERO_BALANCA,
    RAW_ZERO_MAX,
    RAW_ZERO_MIN,
    TARA_MAX,
    TARA_MIN,
)
from .coordinator import BotijaoGasData
from .entity import BotijaoGasEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    data: BotijaoGasData = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    async_add_entities(
        [
            TaraNumber(data, entry),
            AjusteNumber(data, entry),
            ZeroBalancaNumber(data, entry),
            LimiteAlertaNumber(data, entry),
        ]
    )


class _BaseNumber(BotijaoGasEntity, RestoreNumber):
    """Base: restaura o valor salvo ao reiniciar o HA e propaga para o
    BotijaoGasData sempre que o usuário altera o valor pela UI."""

    _attr_mode = NumberMode.BOX

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_data = await self.async_get_last_number_data()
        if last_data is not None and last_data.native_value is not None:
            self._set_data_value(last_data.native_value)
        else:
            self._set_data_value(self._default_value())
        self._data.recompute_from_params()

    async def async_set_native_value(self, value: float) -> None:
        self._set_data_value(value)
        self._data.recompute_from_params()
        self.async_write_ha_state()

    def _set_data_value(self, value: float) -> None:
        raise NotImplementedError

    def _default_value(self) -> float:
        raise NotImplementedError


class TaraNumber(_BaseNumber):
    """Peso da estrutura/plataforma da balança (não é o peso do gás).
    Equivalente ao antigo input_number.tara_botijao_de_gas."""

    _attr_translation_key = "tara"
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
    _attr_native_min_value = TARA_MIN
    _attr_native_max_value = TARA_MAX
    _attr_native_step = 0.01
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_TARA)

    @property
    def native_value(self) -> float:
        return self._data.tara

    def _set_data_value(self, value: float) -> None:
        self._data.tara = value

    def _default_value(self) -> float:
        return DEFAULT_TARA


class AjusteNumber(_BaseNumber):
    """Correção fina de calibração, somada/subtraída junto com a tara.
    Equivalente ao antigo input_number.ajuste_da_balanca_de_gas."""

    _attr_translation_key = "ajuste"
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
    _attr_native_min_value = AJUSTE_MIN
    _attr_native_max_value = AJUSTE_MAX
    _attr_native_step = 0.01
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_AJUSTE)

    @property
    def native_value(self) -> float:
        return self._data.ajuste

    def _set_data_value(self, value: float) -> None:
        self._data.ajuste = value

    def _default_value(self) -> float:
        return DEFAULT_AJUSTE


class ZeroBalancaNumber(_BaseNumber):
    """Leitura raw do HX711 quando a balança está vazia (ponto zero).
    Pode ser ajustado manualmente aqui ou automaticamente pelo botão
    'Calibrar Zero'. Antes era um valor fixo (5968) dentro dos templates."""

    _attr_translation_key = "zero_balanca"
    _attr_native_min_value = RAW_ZERO_MIN
    _attr_native_max_value = RAW_ZERO_MAX
    _attr_native_step = 1
    _attr_entity_category = EntityCategory.CONFIG
    _attr_entity_registry_enabled_default = False

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_ZERO_BALANCA)

    @property
    def native_value(self) -> float:
        return self._data.zero_balanca

    def _set_data_value(self, value: float) -> None:
        self._data.zero_balanca = value

    def _default_value(self) -> float:
        return DEFAULT_RAW_ZERO_OFFSET


class LimiteAlertaNumber(_BaseNumber):
    """Peso (kg) abaixo do qual o binary_sensor 'Gás Baixo' liga.
    Antes era um valor fixo (4kg) dentro do template."""

    _attr_translation_key = "limite_alerta"
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
    _attr_native_min_value = ALERT_THRESHOLD_MIN
    _attr_native_max_value = ALERT_THRESHOLD_MAX
    _attr_native_step = 0.5
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_LIMITE_ALERTA)

    @property
    def native_value(self) -> float:
        return self._data.limite_alerta

    def _set_data_value(self, value: float) -> None:
        self._data.limite_alerta = value

    def _default_value(self) -> float:
        return DEFAULT_ALERT_THRESHOLD
