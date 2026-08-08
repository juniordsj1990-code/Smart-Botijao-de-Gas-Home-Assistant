"""Constantes da integração Botijão de Gás.
Autor: juniordsj1990-code
Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
"""
from __future__ import annotations

DOMAIN = "botijao_gas"

# Configuração inicial (config_flow)
CONF_SOURCE_ENTITY = "source_entity"
CONF_CAPACITY = "capacity_kg"
CONF_NAME = "name"

# Opções (options_flow)
CONF_RAW_PER_KG = "raw_per_kg"
CONF_FILTER_WINDOW = "filter_window"
CONF_M3_PER_KG = "m3_per_kg"

# Padrões
DEFAULT_NAME = "Botijão de Gás"
DEFAULT_CAPACITY = 13.0
DEFAULT_RAW_PER_KG = 1000.0
DEFAULT_FILTER_WINDOW = 1
# m³ de gás (fase gasosa) por kg de GLP consumido - referência para botijão P13 no Brasil.
DEFAULT_M3_PER_KG = 0.52

# Valores padrão para as entidades number (restauradas via RestoreEntity depois)
DEFAULT_TARA = 0.0
DEFAULT_AJUSTE = 0.0
DEFAULT_RAW_ZERO_OFFSET = 5968.0
DEFAULT_ALERT_THRESHOLD = 4.0

# Limites das entidades number
TARA_MIN = 0.0
TARA_MAX = 50.0
AJUSTE_MIN = -5.0
AJUSTE_MAX = 5.0
RAW_ZERO_MIN = -100000.0
RAW_ZERO_MAX = 100000.0
ALERT_THRESHOLD_MIN = 0.0
ALERT_THRESHOLD_MAX = 50.0

# Chaves internas usadas no runtime data (hass.data)
DATA_COORDINATOR = "coordinator"

# Identificadores únicos das entidades (sufixos)
KEY_PESO_DISPONIVEL = "peso_disponivel"
KEY_CONSUMO_M3 = "consumo_m3"
KEY_PESO_BRUTO = "peso_bruto"
KEY_VERIFICACAO_RAW = "verificacao_raw"
KEY_PERCENTUAL = "percentual"
KEY_DIAS_EM_USO = "dias_em_uso"
KEY_ESTIMATIVA_ESGOTAMENTO = "estimativa_esgotamento"
KEY_GAS_BAIXO = "gas_baixo"
KEY_TARA = "tara"
KEY_AJUSTE = "ajuste"
KEY_ZERO_BALANCA = "zero_balanca"
KEY_LIMITE_ALERTA = "limite_alerta"
KEY_ULTIMA_TROCA = "ultima_troca"
KEY_BTN_CALIBRAR = "calibrar_zero"
KEY_BTN_TROCADO = "botijao_trocado"
KEY_BTN_NOTIFICAR = "notificar_status"

SIGNAL_UPDATE = f"{DOMAIN}_update"
