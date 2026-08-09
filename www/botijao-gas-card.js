/**
 * Smart Botijão de Gás - Custom Lovelace Card
 * Autor: juniordsj1990-code
 * Repositório: https://github.com/juniordsj1990-code/Smart-Botijao-de-Gas-Home-Assistant
 * Licença: uso pessoal permitido; redistribuição e uso comercial proibidos sem autorização (ver LICENSE).
 *
 * Card visual único para a integração botijao_gas: mostra o botijão como um
 * cilindro com o nível de gás preenchido, peso disponível, percentual em
 * anel, estatísticas rápidas e uma seção retrátil de configurações e ações
 * (calibrar zero, marcar troca).
 *
 * Instalação:
 *   1. Copie este arquivo para config/www/botijao-gas-card.js
 *   2. Configurações > Painéis > Recursos > Adicionar recurso
 *      URL: /local/botijao-gas-card.js   Tipo: Módulo JavaScript
 *   3. Adicione um card com type: custom:botijao-gas-card
 */

const DEFAULT_ENTITIES = {
  peso_disponivel: "sensor.peso_disponivel",
  percentual: "sensor.percentual",
  peso_bruto: "sensor.peso_bruto",
  dias_em_uso: "sensor.dias_em_uso",
  estimativa_esgotamento: "sensor.estimativa_esgotamento",
  gas_baixo: "binary_sensor.gas_baixo",
  verificacao_raw: "sensor.verificacao_raw",
  tara: "number.tara",
  ajuste: "number.ajuste",
  zero_balanca: "number.zero_balanca",
  limite_alerta: "number.limite_alerta",
  ultima_troca: "datetime.ultima_troca",
  calibrar_zero: "button.calibrar_zero",
  botijao_trocado: "button.botijao_trocado",
};

const FIELD_DOMAINS = {
  peso_disponivel: "sensor",
  percentual: "sensor",
  peso_bruto: "sensor",
  dias_em_uso: "sensor",
  estimativa_esgotamento: "sensor",
  gas_baixo: "binary_sensor",
  verificacao_raw: "sensor",
  tara: "number",
  ajuste: "number",
  zero_balanca: "number",
  limite_alerta: "number",
  ultima_troca: "datetime",
  calibrar_zero: "button",
  botijao_trocado: "button",
};

const FIELD_LABELS = {
  peso_disponivel: "Peso Disponível",
  percentual: "Percentual",
  peso_bruto: "Peso Bruto",
  dias_em_uso: "Dias em Uso",
  estimativa_esgotamento: "Estimativa de Esgotamento",
  gas_baixo: "Gás Baixo",
  verificacao_raw: "Verificação Raw",
  tara: "Tara",
  ajuste: "Ajuste Fino",
  zero_balanca: "Zero da Balança",
  limite_alerta: "Limite de Alerta",
  ultima_troca: "Última Troca",
  calibrar_zero: "Botão Calibrar Zero",
  botijao_trocado: "Botão Botijão Trocado",
};

const DEFAULT_ICONS = {
  icon: "mdi:fire",
  calibrar_zero_icon: "mdi:scale-balance",
  botijao_trocado_icon: "mdi:propane-tank",
};

const HIDE_KEYS = [...Object.keys(DEFAULT_ENTITIES), "status"];
const DEFAULT_HIDE = Object.fromEntries(HIDE_KEYS.map((k) => [`hide_${k}`, false]));

const ICONS = {
  dots: '<circle cx="12" cy="5" r="1.4"/><circle cx="12" cy="12" r="1.4"/><circle cx="12" cy="19" r="1.4"/>',
  scale: '<path d="M12 3v18M7 21h10M5 7l3-3 3 3M13 7l3-3 3 3M3 7h6M15 7h6"/><path d="M3 7l-2 5a3 3 0 0 0 6 0L5 7"/><path d="M21 7l-2 5a3 3 0 0 0 6 0l-2-5"/>',
  calendar: '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
  bag: '<path d="M6 8h12l1.2 12.2A2 2 0 0 1 17.2 22H6.8a2 2 0 0 1-2-1.8L6 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
  check: '<circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.3 2.3L16 10"/>',
  warn: '<path d="M12 3 2 21h20L12 3Z"/><path d="M12 10v4M12 17.2v.1"/>',
  gear: '<circle cx="12" cy="12" r="3"/><path d="M19 12a7 7 0 0 0-.15-1.44l2.02-1.57-2-3.46-2.38.96A7 7 0 0 0 14.94 5l-.36-2.5h-4l-.36 2.5c-.9.28-1.73.72-2.55 1.29l-2.38-.96-2 3.46 2.02 1.57C5.15 10.56 5 11 5 12s.15 1.44.36 1.94l-2.02 1.57 2 3.46 2.38-.96c.7.57 1.53 1 2.44 1.3l.36 2.5h4l.36-2.5c.9-.28 1.73-.72 2.55-1.29l2.38.96 2-3.46-2.02-1.57c.15-.5.24-1 .24-1.5Z"/>',
  chevron: '<path d="M6 9l6 6 6-6"/>',
  pulse: '<path d="M3 12h4l2-8 4 16 2-8h6"/>',
  sliders: '<path d="M4 6h10M4 12h16M4 18h7"/><circle cx="16" cy="6" r="2"/><circle cx="8" cy="18" r="2"/>',
  target: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".8"/>',
  bell: '<path d="M6 10a6 6 0 0 1 12 0c0 4 1.5 5.5 1.5 5.5H4.5S6 14 6 10Z"/><path d="M10 19a2 2 0 0 0 4 0"/>',
  refresh: '<path d="M4 4v5h5"/><path d="M20 20v-5h-5"/><path d="M4.6 15A8 8 0 0 0 19 9"/><path d="M19.4 9A8 8 0 0 0 5 15"/>',
  wifi: '<path d="M2 8.5a16 16 0 0 1 20 0"/><path d="M5.5 12a11 11 0 0 1 13 0"/><path d="M9 15.5a6 6 0 0 1 6 0"/><circle cx="12" cy="19" r="1.2"/>',
};

function icon(name, extraClass) {
  return `<svg class="bg-icon ${extraClass || ""}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${ICONS[name] || ""}</svg>`;
}

function fmt(value, digits) {
  const n = Number(value);
  if (Number.isNaN(n)) return "—";
  return n.toLocaleString("pt-BR", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function relativeTime(isoString) {
  if (!isoString) return "sem dados";
  const then = new Date(isoString).getTime();
  if (Number.isNaN(then)) return "sem dados";
  const diffMin = Math.max(0, Math.round((Date.now() - then) / 60000));
  if (diffMin < 1) return "agora";
  if (diffMin < 60) return `há ${diffMin} minuto${diffMin === 1 ? "" : "s"}`;
  const diffH = Math.round(diffMin / 60);
  if (diffH < 24) return `há ${diffH} hora${diffH === 1 ? "" : "s"}`;
  const diffD = Math.round(diffH / 24);
  return `há ${diffD} dia${diffD === 1 ? "" : "s"}`;
}

function daysAgo(isoString) {
  if (!isoString) return null;
  const then = new Date(isoString).getTime();
  if (Number.isNaN(then)) return null;
  return Math.max(0, Math.round((Date.now() - then) / 86400000));
}

function formatDate(date) {
  return date.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

class BotijaoGasCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._expanded = false;
    this._lastSig = null;
  }

  setConfig(config) {
    this._config = {
      title: "Smart Botijão de Gás",
      subtitle: "Home Assistant",
      ...DEFAULT_ENTITIES,
      ...DEFAULT_ICONS,
      ...DEFAULT_HIDE,
      ...config,
    };
    this._expanded = !!this._config.expanded_by_default;
  }

  getCardSize() {
    return 8;
  }

  static getConfigElement() {
    return document.createElement("botijao-gas-card-editor");
  }

  static getStubConfig() {
    return { type: "custom:botijao-gas-card", ...DEFAULT_ENTITIES };
  }

  set hass(hass) {
    this._hass = hass;
    const c = this._config;
    if (!c) return;

    const ids = [
      c.peso_disponivel, c.percentual, c.peso_bruto, c.dias_em_uso,
      c.estimativa_esgotamento, c.gas_baixo, c.verificacao_raw, c.tara,
      c.ajuste, c.zero_balanca, c.limite_alerta, c.ultima_troca,
    ];
    const sig = ids.map((id) => {
      const st = hass.states[id];
      return st ? `${id}:${st.state}` : `${id}:_`;
    }).join("|") + `|${this._expanded}`;

    if (sig === this._lastSig) return;
    this._lastSig = sig;
    this._render();
  }

  _st(entityId) {
    return this._hass && this._hass.states[entityId];
  }

  _num(entityId, fallback) {
    const st = this._st(entityId);
    if (!st || st.state === "unknown" || st.state === "unavailable") return fallback;
    const n = Number(st.state);
    return Number.isNaN(n) ? fallback : n;
  }

  _callButton(entityId) {
    if (!this._hass) return;
    this._hass.callService("button", "press", { entity_id: entityId });
  }

  _moreInfo(entityId) {
    const ev = new CustomEvent("hass-more-info", {
      detail: { entityId },
      bubbles: true,
      composed: true,
    });
    this.shadowRoot.dispatchEvent(ev);
  }

  _toggle() {
    this._expanded = !this._expanded;
    this._lastSig = null;
    this._render();
  }

  _render() {
    if (!this._hass || !this._config) return;
    const c = this._config;

    const pesoDisponivel = this._num(c.peso_disponivel, 0);
    const percentual = this._num(c.percentual, 0);
    const pesoBruto = this._num(c.peso_bruto, 0);
    const diasEmUso = this._num(c.dias_em_uso, null);
    const estimativaDias = this._num(c.estimativa_esgotamento, null);
    const estimativaState = this._st(c.estimativa_esgotamento);
    const estimativaStatus = estimativaState && estimativaState.attributes
      ? estimativaState.attributes.status : "sem_dados";
    const gasBaixoSt = this._st(c.gas_baixo);
    const gasBaixo = gasBaixoSt ? gasBaixoSt.state === "on" : false;
    const verificacaoRaw = this._num(c.verificacao_raw, 0);
    const tara = this._num(c.tara, 0);
    const ajuste = this._num(c.ajuste, 0);
    const zeroBalanca = this._num(c.zero_balanca, 0);
    const limiteAlerta = this._num(c.limite_alerta, 0);
    const ultimaTrocaSt = this._st(c.ultima_troca);
    const ultimaTrocaISO = ultimaTrocaSt ? ultimaTrocaSt.state : null;
    const diasDesdeTroca = daysAgo(ultimaTrocaISO);

    const sourceUnavailable = !gasBaixoSt || gasBaixoSt.state === "unavailable";
    const lastUpdated = gasBaixoSt ? gasBaixoSt.last_changed : null;

    const statusColor = gasBaixo ? "red" : "green";
    const statusLabel = gasBaixo ? "Atenção" : "Normal";
    const statusCaption = gasBaixo ? "Nível abaixo do limite configurado" : "Tudo dentro do esperado";

    let estimativaLabel = "sem dados";
    let estimativaCaption = "dados insuficientes";
    if (estimativaStatus === "cheio") {
      estimativaLabel = "Botijão cheio";
      estimativaCaption = "sem estimativa necessária";
    } else if (estimativaStatus === "calculado" && estimativaDias !== null) {
      const future = new Date(Date.now() + estimativaDias * 86400000);
      estimativaLabel = formatDate(future);
      estimativaCaption = `em ${estimativaDias} dia${estimativaDias === 1 ? "" : "s"}`;
    }

    const ringPct = Math.max(0, Math.min(100, percentual));
    const ringColor = gasBaixo ? "var(--bg-red)" : "var(--bg-green)";
    const R = 42;
    const CIRC = 2 * Math.PI * R;
    const dash = (ringPct / 100) * CIRC;

    const fillPct = Math.max(2, Math.min(100, percentual));
    const liquidColor = gasBaixo ? "var(--bg-red)" : "var(--bg-green)";

    const H = (key) => !!c[`hide_${key}`];
    const group = (className, items) =>
      items.length
        ? `<div class="${className}" style="grid-template-columns:repeat(${items.length},1fr)">${items.join("")}</div>`
        : "";

    // --- topo: peso disponível + anel de percentual ---
    const topTiles = [];
    if (!H("peso_disponivel")) {
      topTiles.push(`
        <div class="tile">
          <div class="tile-label">Peso Disponível</div>
          ${icon("scale", "c-green")}
          <div class="tile-value c-green">${fmt(pesoDisponivel, 2)}<span class="unit">kg</span></div>
          <div class="tile-caption">de gás restante</div>
        </div>`);
    }
    if (!H("percentual")) {
      topTiles.push(`
        <div class="tile ring-tile">
          <div class="tile-label">Percentual</div>
          <svg class="ring" viewBox="0 0 100 100">
            <circle class="ring-bg" cx="50" cy="50" r="${R}"></circle>
            <circle class="ring-fg" cx="50" cy="50" r="${R}"
              stroke-dasharray="${dash} ${CIRC - dash}"
              style="stroke:${ringColor}"></circle>
          </svg>
          <div class="ring-center">
            <span class="ring-value">${Math.round(ringPct)}<small>%</small></span>
            <span class="ring-caption">restante</span>
          </div>
        </div>`);
    }
    const statColHtml = group("stat-col", topTiles);
    const bodyCols = statColHtml ? "130px 1fr" : "1fr";

    // --- dias em uso / estimativa / peso bruto ---
    const g3 = [];
    if (!H("dias_em_uso")) {
      g3.push(`
        <div class="tile">
          <div class="tile-label">Dias em Uso</div>
          ${icon("calendar", "c-blue")}
          <div class="tile-value">${diasEmUso === null ? "—" : diasEmUso}</div>
          <div class="tile-caption">dias</div>
        </div>`);
    }
    if (!H("estimativa_esgotamento")) {
      g3.push(`
        <div class="tile">
          <div class="tile-label">Estimativa de Esgotamento</div>
          ${icon("clock", "c-orange")}
          <div class="tile-value small">${estimativaLabel}</div>
          <div class="tile-caption">${estimativaCaption}</div>
        </div>`);
    }
    if (!H("peso_bruto")) {
      g3.push(`
        <div class="tile">
          <div class="tile-label">Peso Bruto</div>
          ${icon("bag", "c-purple")}
          <div class="tile-value">${fmt(pesoBruto, 2)}<span class="unit">kg</span></div>
          <div class="tile-caption">peso total (sem tara)</div>
        </div>`);
    }
    const grid3Html = group("grid3", g3);

    // --- status / gás baixo ---
    const g2 = [];
    if (!H("status")) {
      g2.push(`
        <div class="status-tile">
          ${icon("check", `status-icon c-${statusColor}`)}
          <div>
            <div class="status-label">Status</div>
            <div class="status-value c-${statusColor}">${statusLabel}</div>
            <div class="status-caption">${statusCaption}</div>
          </div>
        </div>`);
    }
    if (!H("gas_baixo")) {
      g2.push(`
        <div class="status-tile">
          ${icon("warn", `status-icon c-${gasBaixo ? "red" : "green"}`)}
          <div>
            <div class="status-label">Gás Baixo</div>
            <div class="status-value c-${gasBaixo ? "red" : "green"}">${gasBaixo ? "Sim" : "Não"}</div>
            <div class="status-caption">${gasBaixo ? "abaixo do limite configurado" : "nível dentro da segurança"}</div>
          </div>
        </div>`);
    }
    const grid2Html = group("grid2", g2);

    // --- detalhes: verificação raw / tara / ajuste / zero da balança ---
    const g4 = [];
    if (!H("verificacao_raw")) {
      g4.push(`
        <div class="tile">
          <div class="tile-label">Verificação Raw</div>
          ${icon("pulse", "c-blue")}
          <div class="tile-value small">${fmt(verificacaoRaw, 0)}</div>
          <div class="tile-caption">valor bruto</div>
        </div>`);
    }
    if (!H("tara")) {
      g4.push(`
        <div class="tile">
          <div class="tile-label">Tara</div>
          ${icon("scale", "c-blue")}
          <div class="tile-value small">${fmt(tara, 2)}<span class="unit">kg</span></div>
          <div class="tile-caption">peso do recipiente</div>
        </div>`);
    }
    if (!H("ajuste")) {
      g4.push(`
        <div class="tile">
          <div class="tile-label">Ajuste Fino</div>
          ${icon("sliders", "c-blue")}
          <div class="tile-value small">${ajuste >= 0 ? "+" : ""}${fmt(ajuste, 2)}<span class="unit">kg</span></div>
          <div class="tile-caption">correção aplicada</div>
        </div>`);
    }
    if (!H("zero_balanca")) {
      g4.push(`
        <div class="tile">
          <div class="tile-label">Zero da Balança</div>
          ${icon("target", "c-blue")}
          <div class="tile-value small">${fmt(zeroBalanca, 0)}</div>
          <div class="tile-caption">ponto de zero</div>
        </div>`);
    }
    const grid4Html = group("grid4", g4);

    // --- detalhes: limite de alerta / última troca / calibrar zero ---
    const g3b = [];
    if (!H("limite_alerta")) {
      g3b.push(`
        <div class="status-tile compact">
          ${icon("bell", "status-icon c-orange")}
          <div>
            <div class="status-label">Limite de Alerta</div>
            <div class="status-value small">${fmt(limiteAlerta, 1)}<span class="unit"> kg</span></div>
            <div class="status-caption">peso mínimo antes do alerta</div>
          </div>
        </div>`);
    }
    if (!H("ultima_troca")) {
      g3b.push(`
        <div class="status-tile compact">
          ${icon("calendar", "status-icon c-green")}
          <div>
            <div class="status-label">Última Troca</div>
            <div class="status-value small">${ultimaTrocaISO ? formatDate(new Date(ultimaTrocaISO)) : "sem dados"}</div>
            <div class="status-caption">${diasDesdeTroca === null ? "—" : `há ${diasDesdeTroca} dia${diasDesdeTroca === 1 ? "" : "s"}`}</div>
          </div>
        </div>`);
    }
    if (!H("calibrar_zero")) {
      g3b.push(`
        <div class="status-tile compact action-tile">
          <ha-icon class="status-icon c-blue" icon="${c.calibrar_zero_icon}"></ha-icon>
          <div class="action-tile-body">
            <div class="status-label">Calibrar Zero</div>
            <button class="action-btn c-blue-btn" id="calibrar-btn">CALIBRAR</button>
          </div>
        </div>`);
    }
    const grid3bHtml = group("grid3", g3b);

    const actionRowHtml = H("botijao_trocado") ? "" : `
      <div class="action-row">
        <ha-icon class="status-icon c-purple" icon="${c.botijao_trocado_icon}"></ha-icon>
        <div class="action-row-body">
          <div class="status-label">Botijão Trocado</div>
          <div class="status-caption">Marque quando o botijão for substituído por um novo.</div>
        </div>
        <button class="action-btn c-purple-btn" id="trocado-btn">MARCAR TROCA</button>
      </div>`;

    this.shadowRoot.innerHTML = `
      <style>${this._css()}</style>
      <ha-card>
        <div class="header">
          <div class="header-left">
            <div class="flame-badge"><ha-icon icon="${c.icon}"></ha-icon></div>
            <div>
              <div class="title">${c.title}</div>
              <div class="subtitle">${c.subtitle}</div>
            </div>
          </div>
          <button class="icon-btn" id="more-info-btn" title="Mais informações">${icon("dots")}</button>
        </div>

        <div class="body" style="grid-template-columns:${bodyCols}">
          <div class="cylinder-col">
            ${this._cylinderSvg(fillPct, liquidColor)}
          </div>
          ${statColHtml}
        </div>

        ${grid3Html}
        ${grid2Html}

        <button class="section-toggle" id="toggle-btn">
          ${icon("gear")}
          <span>Detalhes e Configurações</span>
          <span class="spacer"></span>
          <span class="chevron ${this._expanded ? "open" : ""}">${icon("chevron")}</span>
        </button>

        <div class="details ${this._expanded ? "open" : ""}">
          ${grid4Html}
          ${grid3bHtml}
          ${actionRowHtml}
        </div>

        <div class="footer">
          <span class="footer-left">${icon("refresh", "footer-icon")} Atualizado ${relativeTime(lastUpdated)}</span>
          <span class="footer-right ${sourceUnavailable ? "c-red" : "c-green"}">
            ${icon("wifi", "footer-icon")} ${sourceUnavailable ? "Offline" : "Online"}
          </span>
        </div>
      </ha-card>
    `;

    const toggleBtn = this.shadowRoot.getElementById("toggle-btn");
    if (toggleBtn) toggleBtn.addEventListener("click", () => this._toggle());

    const calibrarBtn = this.shadowRoot.getElementById("calibrar-btn");
    if (calibrarBtn) calibrarBtn.addEventListener("click", () => this._callButton(c.calibrar_zero));

    const trocadoBtn = this.shadowRoot.getElementById("trocado-btn");
    if (trocadoBtn) trocadoBtn.addEventListener("click", () => this._callButton(c.botijao_trocado));

    const moreInfoBtn = this.shadowRoot.getElementById("more-info-btn");
    if (moreInfoBtn) moreInfoBtn.addEventListener("click", () => this._moreInfo(c.peso_disponivel));
  }

  _cylinderSvg(fillPct, liquidColor) {
    const bodyTop = 40, bodyBottom = 300, bodyLeft = 40, bodyRight = 160;
    const bodyH = bodyBottom - bodyTop;
    const liquidH = (fillPct / 100) * (bodyH - 8);
    const liquidY = bodyBottom - 4 - liquidH;
    return `
      <svg class="cylinder" viewBox="0 0 200 340" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <clipPath id="bodyClip">
            <rect x="${bodyLeft}" y="${bodyTop}" width="${bodyRight - bodyLeft}" height="${bodyH}" rx="26"></rect>
          </clipPath>
          <linearGradient id="steelGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#5a636b"></stop>
            <stop offset="45%" stop-color="#828d96"></stop>
            <stop offset="100%" stop-color="#3f474d"></stop>
          </linearGradient>
        </defs>

        <!-- base -->
        <rect x="30" y="304" width="140" height="16" rx="6" fill="#2a3036"></rect>

        <!-- body -->
        <rect x="${bodyLeft}" y="${bodyTop}" width="${bodyRight - bodyLeft}" height="${bodyH}" rx="26" fill="url(#steelGrad)"></rect>

        <!-- liquid fill, clipped to body shape -->
        <rect x="${bodyLeft}" y="${liquidY}" width="${bodyRight - bodyLeft}" height="${liquidH + 4}"
          fill="${liquidColor}" opacity="0.88" clip-path="url(#bodyClip)"></rect>
        <rect x="${bodyLeft}" y="${liquidY}" width="${bodyRight - bodyLeft}" height="4"
          fill="${liquidColor}" clip-path="url(#bodyClip)"></rect>

        <!-- collar -->
        <rect x="66" y="16" width="68" height="30" rx="10" fill="#828d96"></rect>
        <path d="M74 16 V4 a4 4 0 0 1 4-4 h44 a4 4 0 0 1 4 4 v12" fill="none" stroke="#828d96" stroke-width="8" stroke-linecap="round"></path>
        <rect x="88" y="-6" width="24" height="16" rx="4" fill="#b9c1c7"></rect>
        <circle cx="100" cy="6" r="7" fill="#c98a2c"></circle>
      </svg>
    `;
  }

  _css() {
    return `
      :host {
        --bg-green: #34d399;
        --bg-red: #f87171;
        --bg-orange: #fb923c;
        --bg-blue: #4f9eff;
        --bg-purple: #a78bfa;
      }
      ha-card {
        background: #0b0f14;
        border: 1px solid #1c242c;
        border-radius: 18px;
        color: #e7edf1;
        font-family: var(--paper-font-body1_-_font-family, "Segoe UI", Roboto, sans-serif);
        padding: 18px 18px 14px;
        overflow: hidden;
      }
      .c-green{color:var(--bg-green)} .c-red{color:var(--bg-red)}
      .c-orange{color:var(--bg-orange)} .c-blue{color:var(--bg-blue)} .c-purple{color:var(--bg-purple)}

      .header{ display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; }
      .header-left{ display:flex; align-items:center; gap:12px; }
      .flame-badge{
        width:38px; height:38px; border-radius:50%;
        background: rgba(79,158,255,0.12); display:flex; align-items:center; justify-content:center;
        color: var(--bg-blue);
      }
      .flame-badge svg, .flame-badge ha-icon{ width:20px; height:20px; --mdc-icon-size:20px; }
      .title{ font-size:1.05rem; font-weight:700; color:#fff; line-height:1.2; }
      .subtitle{ font-size:0.8rem; color:#7c8a94; margin-top:2px; }
      .icon-btn{
        background:none; border:none; color:#7c8a94; cursor:pointer;
        width:32px; height:32px; display:flex; align-items:center; justify-content:center; border-radius:8px;
      }
      .icon-btn:hover{ background:#151c22; color:#e7edf1; }
      .icon-btn svg{ width:18px; height:18px; }

      .body{ display:grid; grid-template-columns: 130px 1fr; gap:16px; margin-bottom:14px; }
      .cylinder-col{ display:flex; align-items:center; justify-content:center; }
      .cylinder{ width:100%; max-width:130px; height:auto; }

      .stat-col{ display:grid; grid-template-columns: 1fr 1fr; gap:12px; }
      .tile{
        background:#12181f; border:1px solid #1c242c; border-radius:12px;
        padding:12px 12px 14px; position:relative; min-width:0;
      }
      .tile-label{ font-size:0.76rem; color:#9aa7b0; margin-bottom:6px; font-weight:600; }
      .bg-icon{ width:18px; height:18px; margin-bottom:6px; }
      .tile-value{ font-size:1.5rem; font-weight:800; color:#fff; line-height:1.1; }
      .tile-value.small{ font-size:1.05rem; }
      .tile-value .unit{ font-size:0.78rem; font-weight:600; color:#9aa7b0; margin-left:4px; }
      .tile-caption{ font-size:0.72rem; color:#7c8a94; margin-top:4px; }

      .ring-tile{ display:flex; flex-direction:column; align-items:center; text-align:center; }
      .ring-tile .tile-label{ align-self:flex-start; }
      .ring{ width:92px; height:92px; transform: rotate(-90deg); margin-top:2px; }
      .ring-bg{ fill:none; stroke:#1c242c; stroke-width:9; }
      .ring-fg{ fill:none; stroke-width:9; stroke-linecap:round; transition: stroke-dasharray .4s ease; }
      .ring-center{ margin-top:-70px; display:flex; flex-direction:column; align-items:center; }
      .ring-value{ font-size:1.5rem; font-weight:800; color:#fff; }
      .ring-value small{ font-size:0.85rem; font-weight:600; color:#9aa7b0; margin-left:1px; }
      .ring-caption{ font-size:0.7rem; color:#7c8a94; margin-top:-2px; }

      .grid3{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:14px; }
      .grid4{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:12px; }
      .grid2{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px; }

      .status-tile{
        background:#12181f; border:1px solid #1c242c; border-radius:12px;
        padding:14px; display:flex; align-items:flex-start; gap:12px;
      }
      .status-tile.compact{ padding:12px; }
      .status-icon{ width:26px; height:26px; flex:none; margin-top:2px; --mdc-icon-size:26px; }
      .status-label{ font-size:0.78rem; color:#9aa7b0; font-weight:600; margin-bottom:2px; }
      .status-value{ font-size:1.05rem; font-weight:800; color:#fff; }
      .status-value.small{ font-size:0.95rem; }
      .status-value .unit{ font-size:0.72rem; color:#9aa7b0; font-weight:600; }
      .status-caption{ font-size:0.72rem; color:#7c8a94; margin-top:3px; }

      .action-tile{ align-items:center; }
      .action-tile-body{ display:flex; flex-direction:column; gap:6px; }
      .action-btn{
        border:none; border-radius:8px; padding:7px 10px; font-size:0.72rem; font-weight:700;
        letter-spacing:0.03em; cursor:pointer; color:#fff;
      }
      .c-blue-btn{ background: rgba(79,158,255,0.18); color:var(--bg-blue); }
      .c-blue-btn:hover{ background: rgba(79,158,255,0.28); }
      .c-purple-btn{ background: rgba(167,139,250,0.85); color:#1c1130; }
      .c-purple-btn:hover{ background: rgba(167,139,250,1); }

      .action-row{
        background:#12181f; border:1px solid #1c242c; border-radius:12px;
        padding:14px; display:flex; align-items:center; gap:12px; margin-bottom:2px;
      }
      .action-row-body{ flex:1; min-width:0; }

      .section-toggle{
        width:100%; display:flex; align-items:center; gap:10px;
        background:#12181f; border:1px solid #1c242c; border-radius:12px;
        padding:12px 14px; color:#e7edf1; font-size:0.86rem; font-weight:600;
        cursor:pointer; margin-bottom:0;
      }
      .section-toggle svg:first-child{ width:16px; height:16px; color:#9aa7b0; }
      .spacer{ flex:1; }
      .chevron svg{ width:16px; height:16px; color:#9aa7b0; transition: transform .2s ease; }
      .chevron.open svg{ transform: rotate(180deg); }

      .details{
        max-height:0; overflow:hidden; transition: max-height .28s ease, margin .28s ease, opacity .2s ease;
        opacity:0; margin-top:0;
      }
      .details.open{ max-height:600px; opacity:1; margin-top:12px; }

      .footer{
        display:flex; justify-content:space-between; align-items:center;
        margin-top:14px; padding-top:12px; border-top:1px solid #1c242c;
        font-size:0.74rem; color:#7c8a94;
      }
      .footer-icon{ width:13px; height:13px; vertical-align:-2px; margin-right:4px; }
      .footer-left, .footer-right{ display:flex; align-items:center; }

      @media (max-width: 420px){
        .body{ grid-template-columns: 1fr; }
        .cylinder-col{ margin-bottom:4px; }
        .cylinder{ max-width:100px; }
        .grid3, .grid4{ grid-template-columns:repeat(2,1fr); }
      }
    `;
  }
}

customElements.define("botijao-gas-card", BotijaoGasCard);

class BotijaoGasCardEditor extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._built = false;
  }

  setConfig(config) {
    this._config = {
      title: "Smart Botijão de Gás",
      subtitle: "Home Assistant",
      ...DEFAULT_ENTITIES,
      ...DEFAULT_ICONS,
      ...DEFAULT_HIDE,
      ...config,
    };
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
    // Os seletores de ícone e de entidade precisam do hass mais recente pra
    // busca funcionar, mesmo depois do formulário já ter sido montado uma vez.
    if (this._built) {
      this.shadowRoot.querySelectorAll("ha-icon-picker, ha-entity-picker").forEach((el) => {
        el.hass = hass;
      });
    }
  }

  _render() {
    if (!this._hass || !this._config) return;

    // Evita reconstruir o DOM inteiro a cada tecla digitada nos campos de texto:
    // só reconstrói na primeira vez; depois disso, os selects já têm o valor certo
    // via `value` e os inputs de texto mantêm o próprio valor digitado pelo usuário.
    if (this._built) return;
    this._built = true;

    const textField = (key, label) => `
      <label class="field">
        <span>${label}</span>
        <input type="text" data-key="${key}" data-kind="text" value="${(this._config[key] || "").replace(/"/g, "&quot;")}">
      </label>`;

    const hideCheckbox = (key) => `
      <label class="hide-toggle">
        <input type="checkbox" data-key="hide_${key}" data-kind="checkbox" ${this._config[`hide_${key}`] ? "checked" : ""}>
        <span>Ocultar</span>
      </label>`;

    const entitySelect = (key) => {
      const domain = FIELD_DOMAINS[key];
      return `
        <div class="field-row">
          <div class="field" id="entity-slot-${key}"><span>${FIELD_LABELS[key]} <em>(${domain})</em></span></div>
          ${hideCheckbox(key)}
        </div>`;
    };

    this.shadowRoot.innerHTML = `
      <style>
        .wrap{ display:flex; flex-direction:column; gap:14px; padding:8px 2px; font-family: var(--paper-font-body1_-_font-family, sans-serif); }
        .group{ display:flex; flex-direction:column; gap:8px; }
        .group-title{ font-size:0.8rem; font-weight:700; color: var(--secondary-text-color, #888); text-transform:uppercase; letter-spacing:.04em; margin-top:6px; }
        .field{ display:flex; flex-direction:column; gap:4px; font-size:0.86rem; color: var(--primary-text-color, #333); }
        .field em{ font-weight:400; font-style:normal; color: var(--secondary-text-color, #888); font-size:0.76rem; }
        input, select{
          padding:8px 10px; border-radius:8px; border:1px solid var(--divider-color, #ccc);
          background: var(--card-background-color, #fff); color: var(--primary-text-color, #333);
          font-size:0.86rem;
        }
        .hint{ font-size:0.76rem; color: var(--secondary-text-color, #888); margin-top:-6px; }
        ha-icon-picker, ha-entity-picker{ width:100%; }
        .field-row{ display:flex; align-items:flex-end; gap:10px; }
        .field-row .field{ flex:1; min-width:0; }
        .hide-toggle{
          display:flex; align-items:center; gap:5px; font-size:0.78rem;
          color: var(--secondary-text-color, #888); white-space:nowrap; padding-bottom:8px;
        }
        .hide-toggle input{ width:15px; height:15px; padding:0; }
        .standalone-toggle{
          display:flex; align-items:center; justify-content:space-between;
          font-size:0.86rem; color: var(--primary-text-color, #333);
          border:1px solid var(--divider-color, #ccc); border-radius:8px; padding:8px 10px;
        }
      </style>
      <div class="wrap">
        <div class="group">
          <div class="group-title">Aparência</div>
          ${textField("title", "Título")}
          ${textField("subtitle", "Subtítulo")}
        </div>

        <div class="group">
          <div class="group-title">Ícones</div>
          <div class="hint">Clique pra buscar em todo o catálogo de ícones do Home Assistant.</div>
          <div class="field" id="icon-slot-icon"><span>Ícone do cabeçalho</span></div>
          <div class="field" id="icon-slot-calibrar_zero_icon"><span>Ícone do botão Calibrar Zero</span></div>
          <div class="field" id="icon-slot-botijao_trocado_icon"><span>Ícone do botão Botijão Trocado</span></div>
        </div>

        <div class="group">
          <div class="group-title">Entidades principais</div>
          <div class="hint">Deixados em branco assumem os nomes padrão da integração.</div>
          ${entitySelect("peso_disponivel")}
          ${entitySelect("percentual")}
          ${entitySelect("peso_bruto")}
          ${entitySelect("dias_em_uso")}
          ${entitySelect("estimativa_esgotamento")}
          ${entitySelect("gas_baixo")}
          <label class="standalone-toggle">
            <span>Ocultar tile "Status" (derivado de Gás Baixo)</span>
            <input type="checkbox" data-key="hide_status" data-kind="checkbox" ${this._config.hide_status ? "checked" : ""}>
          </label>
        </div>

        <div class="group">
          <div class="group-title">Detalhes e configurações</div>
          ${entitySelect("verificacao_raw")}
          ${entitySelect("tara")}
          ${entitySelect("ajuste")}
          ${entitySelect("zero_balanca")}
          ${entitySelect("limite_alerta")}
          ${entitySelect("ultima_troca")}
          ${entitySelect("calibrar_zero")}
          ${entitySelect("botijao_trocado")}
        </div>
      </div>
    `;

    this.shadowRoot.querySelectorAll("[data-key]").forEach((el) => {
      const kind = el.getAttribute("data-kind");
      const evt = kind === "checkbox" || el.tagName === "SELECT" ? "change" : "input";
      el.addEventListener(evt, (e) => this._onFieldChange(e));
    });

    ["icon", "calibrar_zero_icon", "botijao_trocado_icon"].forEach((key) => {
      this._mountIconPicker(key);
    });

    Object.keys(FIELD_DOMAINS).forEach((key) => {
      this._mountEntityPicker(key);
    });
  }

  _mountEntityPicker(key) {
    const slot = this.shadowRoot.getElementById(`entity-slot-${key}`);
    if (!slot) return;
    const domain = FIELD_DOMAINS[key];
    const picker = document.createElement("ha-entity-picker");
    picker.hass = this._hass;
    picker.value = this._config[key] || "";
    picker.includeDomains = [domain];
    picker.allowCustomEntity = true;
    picker.label = `${FIELD_LABELS[key]} (${domain})`;
    picker.addEventListener("value-changed", (e) => {
      e.stopPropagation();
      const value = e.detail.value || "";
      this._config = { ...this._config, [key]: value };
      this.dispatchEvent(
        new CustomEvent("config-changed", {
          detail: { config: this._config },
          bubbles: true,
          composed: true,
        })
      );
    });
    slot.appendChild(picker);
  }

  _mountIconPicker(key) {
    const slot = this.shadowRoot.getElementById(`icon-slot-${key}`);
    if (!slot) return;
    const picker = document.createElement("ha-icon-picker");
    picker.hass = this._hass;
    picker.value = this._config[key] || "";
    picker.addEventListener("value-changed", (e) => {
      e.stopPropagation();
      this._config = { ...this._config, [key]: e.detail.value };
      this.dispatchEvent(
        new CustomEvent("config-changed", {
          detail: { config: this._config },
          bubbles: true,
          composed: true,
        })
      );
    });
    slot.appendChild(picker);
  }

  _onFieldChange(e) {
    const key = e.target.getAttribute("data-key");
    const kind = e.target.getAttribute("data-kind");
    const value = kind === "checkbox" ? e.target.checked : e.target.value;
    this._config = { ...this._config, [key]: value };
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: this._config },
        bubbles: true,
        composed: true,
      })
    );
  }
}

customElements.define("botijao-gas-card-editor", BotijaoGasCardEditor);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "botijao-gas-card",
  name: "Botijão de Gás",
  description: "Card visual para a integração botijao_gas: nível, peso, percentual e ações de calibração.",
  preview: false,
});
