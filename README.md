# Botijão de Gás – Integração para Home Assistant

![botijao_gas](https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant/blob/main/botijao_gas_integration/assets/icon.png)

[![Repositório](https://img.shields.io/badge/GitHub-Smart--Botijao--de--Gas--Home--Assistant-blue)](https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant)
[![Autor](https://img.shields.io/badge/autor-juniordsj1990--code-orange)](https://github.com/juniordsj1990-code)
[![Licença](https://img.shields.io/badge/licença-uso%20pessoal%20·%20sem%20redistribuição-red)](LICENSE)

Integração custom para transformar a leitura de uma balança HX711 (via Tasmota) em peso, percentual, dias em uso e estimativa de esgotamento do botijão de gás.

Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant

## Instalação

### Via HACS (recomendado)

1. HACS → menu (⋮) → **Repositórios personalizados**
2. Cole a URL `https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant`, categoria **Integração**
3. Instale **Botijão de Gás** pela busca do HACS e reinicie o Home Assistant

### Manual

1. Copie a pasta `custom_components/botijao_gas` para dentro de
   `config/custom_components/` na sua instalação do Home Assistant.
2. Reinicie o Home Assistant.
3. Vá em **Configurações → Dispositivos e Serviços → Adicionar Integração**
   e procure por **Botijão de Gás**.
4. Selecione o sensor de origem — o `HX711 WeightRaw` que já vem da
   integração Tasmota (ex.: `sensor.balanca_botijao_de_gas_hx711_weightraw`)
   — e informe a capacidade do botijão (padrão 13 kg).

Depois de criada, clique em **Configurar** na integração para ajustar as
opções avançadas (fator de escala raw→kg e janela do filtro de média
móvel).

## Entidades criadas

Todas agrupadas sob um único dispositivo "Botijão de Gás":

- **sensor.peso_disponivel** – peso real de gás disponível (kg)
- **sensor.peso_bruto** – peso convertido sem descontar tara/ajuste (kg, diagnóstico)
- **sensor.verificacao_raw** – valor bruto de diagnóstico (desabilitado por padrão)
- **sensor.percentual** – percentual de gás restante
- **sensor.dias_em_uso** – dias desde a última troca
- **sensor.estimativa_esgotamento** – dias estimados até acabar (atributo `status`: `sem_dados` / `cheio` / `calculado`)
- **sensor.consumo_m3** – consumo acumulado desde o botijão cheio, em m³ (para o Painel de Energia)
- **binary_sensor.gas_baixo** – liga quando o peso fica abaixo do limite de alerta
- **number.tara** – peso da estrutura/plataforma da balança
- **number.ajuste** – correção fina de calibração
- **number.zero_balanca** – leitura raw com a balança vazia (desabilitado por padrão)
- **number.limite_alerta** – limite (kg) para o alerta de gás baixo
- **datetime.ultima_troca** – data/hora da última troca do botijão
- **button.calibrar_zero** – zera a balança automaticamente (calibração assistida)
- **button.botijao_trocado** – reseta a data de última troca para agora
- **button.notificar_status** – dispara uma notificação persistente com o status atual


## Painel de Energia (Consumo de gás)

A entidade **sensor.consumo_m3** foi feita especificamente para a tela
**Configurações → Painéis → Energia → Consumo de gás** do Home Assistant.

Como funciona: o Painel de Energia exige um sensor de volume (m³) que só
aumenta com o tempo (`state_class: total_increasing`) — o padrão de um
medidor físico. Como a balança mede peso (que diminui com o uso), o
`consumo_m3` é calculado como `capacidade − peso_disponível`, convertido
de kg para m³ por um fator configurável (`m³ por kg`, opção da
integração — sugestão inicial de **0,52 m³/kg**, referência para GLP em
botijão P13 no Brasil). Esse valor sobe conforme o gás é consumido e volta
para perto de zero quando você troca o botijão — o HA já reconhece esse
padrão de "reset" como troca de medidor e soma o consumo corretamente ao
longo do tempo, sem exigir nenhuma configuração extra da sua parte.

Se preferir um fator mais preciso pro seu gás (a densidade varia um pouco
com a proporção propano/butano da mistura), ajuste em **Configurar** na
integração.

**Observação:** essa conversão é uma estimativa baseada em peso, não uma
medição direta de vazão como um medidor de gás encanado. Serve bem para
acompanhar tendência de consumo e comparar no Painel de Energia, mas não
tem a mesma precisão de um medidor físico de volume.

## Autor

Desenvolvido e mantido por **[juniordsj1990-code](https://github.com/juniordsj1990-code)**.

Repositório oficial: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant

Se você encontrou este código fora do repositório acima, é uma cópia não
autorizada — veja o [`LICENSE`](LICENSE) e o [`AUTHORS`](AUTHORS) para os
termos de uso, e por favor avise o autor.

## Licença

Este projeto é distribuído sob uma **licença de uso pessoal** (não é MIT
nem outra licença OSI padrão): você pode instalar, usar e modificar para
sua própria instalação do Home Assistant, mas redistribuição, publicação
sob outra autoria e uso comercial exigem autorização prévia do autor.
Termos completos em [`LICENSE`](LICENSE).
