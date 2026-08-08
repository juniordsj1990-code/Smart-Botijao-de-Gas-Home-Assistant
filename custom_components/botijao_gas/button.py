"""Botões: calibrar zero, registrar troca do botijão e notificar status.
Autor: juniordsj1990-code
Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
"""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DATA_COORDINATOR,
    DOMAIN,
    KEY_BTN_CALIBRAR,
    KEY_BTN_NOTIFICAR,
    KEY_BTN_TROCADO,
)
from .coordinator import BotijaoGasData
from .entity import BotijaoGasEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    data: BotijaoGasData = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    async_add_entities(
        [
            CalibrarZeroButton(data, entry),
            BotijaoTrocadoButton(data, entry),
            NotificarStatusButton(data, entry),
        ]
    )


class CalibrarZeroButton(BotijaoGasEntity, ButtonEntity):
    """Calibração assistida: com a plataforma vazia (sem botijão em cima),
    pressione este botão para zerar a balança automaticamente."""

    _attr_translation_key = "calibrar_zero"
    _attr_icon = "mdi:scale-balance"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_BTN_CALIBRAR)

    async def async_press(self) -> None:
        self._data.calibrar_zero()


class BotijaoTrocadoButton(BotijaoGasEntity, ButtonEntity):
    """Pressione ao trocar o botijão: reseta a data de 'Última Troca' para
    agora, usada no cálculo de Dias em Uso e Estimativa de Esgotamento."""

    _attr_translation_key = "botijao_trocado"
    _attr_icon = "mdi:propane-tank"

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_BTN_TROCADO)

    async def async_press(self) -> None:
        self._data.registrar_troca()


class NotificarStatusButton(BotijaoGasEntity, ButtonEntity):
    """Dispara uma notificação persistente com o status atual do botijão
    (peso, percentual e estimativa). Equivalente ao antigo
    input_button.status_do_botijao_de_gas."""

    _attr_translation_key = "notificar_status"
    _attr_icon = "mdi:bell-alert"

    def __init__(self, data: BotijaoGasData, entry: ConfigEntry) -> None:
        super().__init__(data, entry, KEY_BTN_NOTIFICAR)

    async def async_press(self) -> None:
        d = self._data
        if d.estimativa_status == "cheio":
            estimativa_txt = "botijão cheio."
        elif d.estimativa_status == "calculado":
            estimativa_txt = f"previsão de acabar em {d.estimativa_esgotamento} dia(s)."
        else:
            estimativa_txt = "sem dados suficientes para estimar."

        message = (
            f"Peso disponível: {d.peso_disponivel:.2f} kg "
            f"({d.percentual:.1f}%). "
            f"Em uso há {d.dias_em_uso if d.dias_em_uso is not None else '—'} dia(s). "
            f"Estimativa: {estimativa_txt}"
        )

        await self.hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": "Status do Botijão de Gás",
                "message": message,
                "notification_id": f"{DOMAIN}_status_{self._entry.entry_id}",
            },
            blocking=True,
        )
