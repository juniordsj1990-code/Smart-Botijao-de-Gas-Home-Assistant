"""Sensores da integração Botijão de Gás.
Autor: juniordsj1990-code
Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
"""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfMass, UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DATA_COORDINATOR,
    DOMAIN,
    KEY_CONSUMO_M3,
    KEY_DIAS_EM_USO,
    KEY_ESTIMATIVA_ESGOTAMENTO,
    KEY_PERCENTUAL,
    KEY_PESO_BRUTO,
    KEY_PESO_DISPONIVEL,
    KEY_VERIFICACAO_RAW,
)
from .coordinator import BotijaoGasData
from .entity import BotijaoGasEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    data: BotijaoGasData = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    async_add_entities(
        [
            PesoDisponivelSensor(data, entry),
            PesoBrutoSensor(data, entry),
            VerificacaoRawSensor(data, entry),
            PercentualSensor(data, entry),
            DiasEmUsoSensor(data, entry),
            EstimativaEsgotamentoSensor(data, entry),
            ConsumoGasSensor(data, entry),
        ]
    )


class PesoDisponivelSensor(BotijaoGasEntity, SensorEntity):
    """Peso real de gás disponível (carga - tara - ajuste), equivalente ao
    antigo sensor.botijao_de_gas_template_com_filtro."""

    _attr_translation_key = "peso_disponivel"
    _attr_device_class = SensorDeviceClass.WEIGHT
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 2

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_PESO_DISPONIVEL)

    @property
    def native_value(self) -> float:
        return self._data.peso_disponivel


class PesoBrutoSensor(BotijaoGasEntity, SensorEntity):
    """Peso bruto convertido, sem descontar tara/ajuste. Equivalente ao
    antigo sensor.botijao_de_gas_decimal_template."""

    _attr_translation_key = "peso_bruto"
    _attr_device_class = SensorDeviceClass.WEIGHT
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 3
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_PESO_BRUTO)

    @property
    def native_value(self) -> float:
        return self._data.peso_bruto


class VerificacaoRawSensor(BotijaoGasEntity, SensorEntity):
    """Valor bruto de diagnóstico (unidades do HX711, sem escala). Equivalente
    ao antigo sensor.peso_do_gas_disponivel_template_tira_teima_2."""

    _attr_translation_key = "verificacao_raw"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_VERIFICACAO_RAW)

    @property
    def native_value(self) -> float:
        return self._data.verificacao_raw


class PercentualSensor(BotijaoGasEntity, SensorEntity):
    """Percentual de gás restante. Equivalente ao antigo
    sensor.botijao_de_gas_percentual_template."""

    _attr_translation_key = "percentual"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:gas-cylinder"

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_PERCENTUAL)

    @property
    def native_value(self) -> float:
        return self._data.percentual


class DiasEmUsoSensor(BotijaoGasEntity, SensorEntity):
    """Dias desde a última troca. Equivalente ao antigo
    sensor.botijao_de_gas_dias_em_uso_template."""

    _attr_translation_key = "dias_em_uso"
    _attr_native_unit_of_measurement = "d"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:calendar-clock"

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_DIAS_EM_USO)

    @property
    def native_value(self) -> int | None:
        return self._data.dias_em_uso


class EstimativaEsgotamentoSensor(BotijaoGasEntity, SensorEntity):
    """Estimativa de dias restantes até o gás acabar. Equivalente ao antigo
    sensor.botijao_de_gas_estimativa_de_esgotamento_template.

    O valor numérico (dias restantes) fica no estado quando há dados
    suficientes; quando não há, o estado reflete a situação
    ("cheio" ou "sem_dados") - veja o atributo `status`.
    """

    _attr_translation_key = "estimativa_esgotamento"
    _attr_native_unit_of_measurement = "d"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:timer-sand"

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_ESTIMATIVA_ESGOTAMENTO)

    @property
    def native_value(self) -> int | None:
        return self._data.estimativa_esgotamento

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        return {"status": self._data.estimativa_status}


class ConsumoGasSensor(BotijaoGasEntity, SensorEntity):
    """Consumo acumulado de gás, em m³, desde o botijão cheio. Pensado para
    alimentar o Painel de Energia do Home Assistant (Configurações >
    Painéis > Energia > Consumo de gás). Sobe conforme o gás é usado e
    'reseta' para perto de zero quando o botijão é trocado - o HA já
    interpreta esse padrão como a troca de um medidor físico."""

    _attr_translation_key = "consumo_m3"
    _attr_device_class = SensorDeviceClass.GAS
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_suggested_display_precision = 3

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_CONSUMO_M3)

    @property
    def native_value(self) -> float:
        return self._data.consumo_m3
