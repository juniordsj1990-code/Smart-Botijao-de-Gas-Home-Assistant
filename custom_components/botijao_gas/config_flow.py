"""Config flow da integração Botijão de Gás.
Autor: juniordsj1990-code
Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
"""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    TextSelector,
)

from .const import (
    CONF_CAPACITY,
    CONF_FILTER_WINDOW,
    CONF_M3_PER_KG,
    CONF_NAME,
    CONF_RAW_PER_KG,
    CONF_SOURCE_ENTITY,
    DEFAULT_CAPACITY,
    DEFAULT_FILTER_WINDOW,
    DEFAULT_M3_PER_KG,
    DEFAULT_NAME,
    DEFAULT_RAW_PER_KG,
    DOMAIN,
)


class BotijaoGasConfigFlow(ConfigFlow, domain=DOMAIN):
    """Fluxo de configuração inicial."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> Any:
        errors: dict[str, str] = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={
                    CONF_SOURCE_ENTITY: user_input[CONF_SOURCE_ENTITY],
                    CONF_CAPACITY: user_input[CONF_CAPACITY],
                },
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): TextSelector(),
                vol.Required(CONF_SOURCE_ENTITY): EntitySelector(
                    EntitySelectorConfig(domain="sensor")
                ),
                vol.Required(CONF_CAPACITY, default=DEFAULT_CAPACITY): NumberSelector(
                    NumberSelectorConfig(
                        min=1, max=200, step=0.5, unit_of_measurement="kg",
                        mode=NumberSelectorMode.BOX,
                    )
                ),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return BotijaoGasOptionsFlow()


class BotijaoGasOptionsFlow(OptionsFlow):
    """Fluxo de opções avançadas (fator de escala, filtro)."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> Any:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.options
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_RAW_PER_KG,
                    default=current.get(CONF_RAW_PER_KG, DEFAULT_RAW_PER_KG),
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=1, max=1000000, step=1, mode=NumberSelectorMode.BOX
                    )
                ),
                vol.Required(
                    CONF_FILTER_WINDOW,
                    default=current.get(CONF_FILTER_WINDOW, DEFAULT_FILTER_WINDOW),
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=1, max=50, step=1, mode=NumberSelectorMode.BOX
                    )
                ),
                vol.Required(
                    CONF_M3_PER_KG,
                    default=current.get(CONF_M3_PER_KG, DEFAULT_M3_PER_KG),
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=0.1, max=2.0, step=0.01,
                        unit_of_measurement="m³/kg",
                        mode=NumberSelectorMode.BOX,
                    )
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
