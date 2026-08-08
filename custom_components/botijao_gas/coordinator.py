"""Motor de cálculo da integração Botijão de Gás.

Este objeto é o "cérebro": guarda os valores editáveis (tara, ajuste, zero da
balança, limite de alerta, última troca) e recalcula tudo sempre que o sensor
de origem (HX711 WeightRaw) ou algum desses parâmetros muda. As entidades
(sensor/number/button/datetime) só leem e escrevem nele.
Autor: juniordsj1990-code
Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
"""
from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.util import dt as dt_util

from .const import (
    CONF_CAPACITY,
    CONF_FILTER_WINDOW,
    CONF_M3_PER_KG,
    CONF_RAW_PER_KG,
    CONF_SOURCE_ENTITY,
    DEFAULT_AJUSTE,
    DEFAULT_ALERT_THRESHOLD,
    DEFAULT_CAPACITY,
    DEFAULT_FILTER_WINDOW,
    DEFAULT_M3_PER_KG,
    DEFAULT_RAW_PER_KG,
    DEFAULT_RAW_ZERO_OFFSET,
    DEFAULT_TARA,
)

_LOGGER = logging.getLogger(__name__)


class BotijaoGasData:
    """Guarda o estado e a lógica de cálculo do botijão de gás."""

    def __init__(self, hass: HomeAssistant, entry) -> None:
        self.hass = hass
        self.entry = entry

        self.source_entity: str = entry.data[CONF_SOURCE_ENTITY]
        self.capacity: float = entry.data.get(CONF_CAPACITY, DEFAULT_CAPACITY)
        self.raw_per_kg: float = entry.options.get(CONF_RAW_PER_KG, DEFAULT_RAW_PER_KG)
        self.filter_window: int = entry.options.get(
            CONF_FILTER_WINDOW, DEFAULT_FILTER_WINDOW
        )
        self.m3_per_kg: float = entry.options.get(CONF_M3_PER_KG, DEFAULT_M3_PER_KG)

        # Valores editáveis pelo usuário (restaurados pelas entidades number/datetime)
        self.tara: float = DEFAULT_TARA
        self.ajuste: float = DEFAULT_AJUSTE
        self.zero_balanca: float = DEFAULT_RAW_ZERO_OFFSET
        self.limite_alerta: float = DEFAULT_ALERT_THRESHOLD
        self.ultima_troca: datetime | None = None

        self._raw_history: list[float] = []
        self._unsub_source: Callable | None = None
        self._listeners: list[Callable[[], None]] = []

        # Valores calculados (cache, lidos pelos sensores)
        self.peso_disponivel: float = 0.0
        self.peso_bruto: float = 0.0
        self.verificacao_raw: float = 0.0
        self.percentual: float = 0.0
        self.dias_em_uso: int | None = None
        self.estimativa_esgotamento: int | None = None
        # sem_dados | cheio | calculado
        self.estimativa_status: str = "sem_dados"
        self.gas_baixo: bool = False
        self.raw_atual: float | None = None
        # Consumo acumulado desde o botijão cheio, em m³ - para o Painel de
        # Energia do HA (device_class "gas", state_class "total_increasing").
        # Sobe conforme o gás é usado e "reseta" para perto de 0 na troca do
        # botijão, exatamente como um medidor físico que o HA sabe interpretar.
        self.consumo_m3: float = 0.0

        self.device_name: str = entry.title

    # ------------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------------
    def async_setup(self) -> None:
        self._unsub_source = async_track_state_change_event(
            self.hass, [self.source_entity], self._handle_source_update
        )
        state = self.hass.states.get(self.source_entity)
        if state is not None:
            self._recalculate(state.state)
        else:
            self._recalc_tempo()

    def async_unload(self) -> None:
        if self._unsub_source is not None:
            self._unsub_source()
            self._unsub_source = None

    def add_listener(self, callback_fn: Callable[[], None]) -> None:
        self._listeners.append(callback_fn)

    def remove_listener(self, callback_fn: Callable[[], None]) -> None:
        if callback_fn in self._listeners:
            self._listeners.remove(callback_fn)

    def _notify(self) -> None:
        for cb in list(self._listeners):
            cb()

    # ------------------------------------------------------------------
    # Recalculo disparado por mudança de parâmetro (tara, ajuste, etc.)
    # ------------------------------------------------------------------
    def recompute_from_params(self) -> None:
        state = self.hass.states.get(self.source_entity)
        if state is not None:
            self._recalculate(state.state)
        else:
            self._recalc_tempo()
            self._notify()

    # ------------------------------------------------------------------
    # Cálculo principal (equivalente aos templates Jinja originais)
    # ------------------------------------------------------------------
    @callback
    def _handle_source_update(self, event) -> None:
        new_state = event.data.get("new_state")
        if new_state is None:
            return
        self._recalculate(new_state.state)

    def _recalculate(self, raw_state: str) -> None:
        try:
            raw = float(raw_state)
        except (ValueError, TypeError):
            _LOGGER.debug("Estado não numérico ignorado: %s", raw_state)
            return

        self.raw_atual = raw

        # Filtro de média móvel (equivalente ao "sensor com filtro", agora de verdade)
        window = max(1, int(self.filter_window))
        self._raw_history.append(raw)
        if len(self._raw_history) > window:
            self._raw_history = self._raw_history[-window:]
        raw_filtrado = sum(self._raw_history) / len(self._raw_history)

        # Peso bruto em kg, sem tara/ajuste (equivalente ao decimal_template)
        peso_bruto = (raw_filtrado - self.zero_balanca) / self.raw_per_kg
        self.peso_bruto = round(max(peso_bruto, 0.0), 3)

        # Verificação raw - diagnóstico bruto, sem escala (equivalente ao tira_teima_2)
        self.verificacao_raw = max(round(raw_filtrado - self.zero_balanca), 0)

        # Peso disponível = carga real (equivalente ao template_com_filtro)
        carga = round(peso_bruto - self.tara - self.ajuste, 3)
        carga_truncada = int(carga * 100) / 100
        if 0 <= carga_truncada <= self.capacity:
            self.peso_disponivel = carga_truncada
        else:
            self.peso_disponivel = 0.0

        # Consumo acumulado em m³ (capacidade - peso disponível, convertido)
        consumo_kg = max(self.capacity - self.peso_disponivel, 0.0)
        self.consumo_m3 = round(consumo_kg * self.m3_per_kg, 3)

        # Percentual
        self.percentual = (
            round((self.peso_disponivel / self.capacity) * 100, 1)
            if self.capacity
            else 0.0
        )

        # Alerta de gás baixo
        self.gas_baixo = self.peso_disponivel < self.limite_alerta

        self._recalc_tempo()
        self._notify()

    def _recalc_tempo(self) -> None:
        if self.ultima_troca is None:
            self.dias_em_uso = None
            self.estimativa_status = "sem_dados"
            self.estimativa_esgotamento = None
            return

        agora = dt_util.utcnow()
        dias_passados = (agora - self.ultima_troca).total_seconds() / 86400
        self.dias_em_uso = round(dias_passados)

        if self.peso_disponivel >= self.capacity:
            self.estimativa_status = "cheio"
            self.estimativa_esgotamento = None
            return

        if dias_passados <= 0:
            self.estimativa_status = "sem_dados"
            self.estimativa_esgotamento = None
            return

        consumo_diario = (self.capacity - self.peso_disponivel) / dias_passados
        if consumo_diario > 0:
            self.estimativa_esgotamento = round(self.peso_disponivel / consumo_diario)
            self.estimativa_status = "calculado"
        else:
            self.estimativa_status = "sem_dados"
            self.estimativa_esgotamento = None

    # ------------------------------------------------------------------
    # Ações (botões)
    # ------------------------------------------------------------------
    def calibrar_zero(self) -> None:
        """Calibração assistida: zera a balança usando a leitura raw atual."""
        if self.raw_atual is not None:
            self.zero_balanca = self.raw_atual
            self.recompute_from_params()

    def registrar_troca(self) -> None:
        """Reseta a data de última troca para agora."""
        self.ultima_troca = dt_util.utcnow()
        self.recompute_from_params()
