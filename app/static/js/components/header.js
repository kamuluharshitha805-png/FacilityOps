/**
 * Header Component: Global Navigation, Health Score, Persona Switcher & Scenario Trigger
 */

const HeaderComponent = {
  render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `
      <!-- Top Scenario Injection Control Bar -->
      <div class="scenario-bar">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span class="badge badge-purple" style="font-size: 10px;">ANOMALY INJECTION LAB</span>
          <span style="color: #E2E8F0; font-size: 11px;">Test multi-agent cross-correlation by triggering facility incident scenarios:</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <select id="scenario-select" style="background: #0F172A; color: #FFF; border: 1px solid #3730A3; padding: 4px 8px; border-radius: 4px; font-size: 11px;">
            <option value="scenario_reset_nominal">Nominal Baseline (All Systems Normal)</option>
            <option value="scenario_chiller_overheat">🔥 Chiller 2 Bearing Overheat & Vibration (Critical)</option>
            <option value="scenario_restricted_breach">🚨 Data Center Unauthenticated Intrusion (Critical)</option>
            <option value="scenario_water_leak">💧 Rooftop Cooling Tower Water Main Leak (High)</option>
            <option value="scenario_peak_demand_spike">⚡ Peak Tariff Demand Surcharge Spike (High)</option>
          </select>
          <button class="btn btn-purple" style="padding: 4px 10px; font-size: 11px;" onclick="HeaderComponent.handleInjectScenario()">
            ▶ Inject Incident
          </button>
        </div>
      </div>

      <!-- Main Header Navigation Bar -->
      <header style="background: #0B0F17; border-bottom: 1px solid var(--border-subtle); padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
        <!-- Brand Title & Building Info -->
        <div style="display: flex; align-items: center; gap: 14px;">
          <div style="width: 38px; height: 38px; background: linear-gradient(135deg, #0284C7, #4F46E5); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 18px; color: #FFF; box-shadow: 0 0 15px rgba(2, 132, 199, 0.4);">
            FO
          </div>
          <div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <h1 style="font-size: 16px; font-weight: 800; letter-spacing: 0.5px; color: #FFFFFF;">
                FACILITY<span style="color: var(--color-primary);">OPS</span> <span style="font-size: 12px; font-weight: 400; color: var(--text-dim);">AI COMMAND CENTER</span>
              </h1>
              <span id="ws-status-indicator" class="badge badge-healthy">
                <span class="beacon-live"></span> LIVE TELEMETRY
              </span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted); display: flex; align-items: center; gap: 8px; margin-top: 2px;">
              <span>Apex Tower Global HQ</span>
              <span>•</span>
              <span>285,000 sq.ft</span>
              <span>•</span>
              <span id="header-clock" class="mono">--:--:--</span>
            </div>
          </div>
        </div>

        <!-- Global Facility Health Score -->
        <div style="display: flex; align-items: center; gap: 16px;">
          <div class="glass-panel" style="padding: 6px 16px; display: flex; align-items: center; gap: 12px; border-color: rgba(56, 189, 248, 0.3);">
            <div>
              <div style="font-size: 10px; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">FACILITY HEALTH</div>
              <div id="header-health-score" style="font-size: 20px; font-weight: 800; font-family: var(--font-mono); color: var(--color-primary);">
                91.5%
              </div>
            </div>
            <div style="font-size: 11px; color: var(--text-dim); line-height: 1.2;">
              <div>6 Autonomous AI Agents</div>
              <div style="color: var(--color-success); font-weight: 600;">Autonomous Sync Active</div>
            </div>
          </div>

          <!-- Persona / Role Switcher -->
          <div style="display: flex; align-items: center; gap: 6px; background: var(--bg-surface-2); padding: 4px; border-radius: 8px; border: 1px solid var(--border-subtle);">
            <button class="btn btn-outline persona-btn active" data-persona="manager" onclick="HeaderComponent.switchPersona('manager')">
              🏢 Facility Mgr
            </button>
            <button class="btn btn-outline persona-btn" data-persona="maintenance" onclick="HeaderComponent.switchPersona('maintenance')">
              🔧 Maintenance
            </button>
            <button class="btn btn-outline persona-btn" data-persona="security" onclick="HeaderComponent.switchPersona('security')">
              🛡️ Security
            </button>
            <button class="btn btn-outline persona-btn" data-persona="executive" onclick="HeaderComponent.switchPersona('executive')">
              👔 Executive
            </button>
          </div>
        </div>
      </header>
    `;

    this.startClock();
  },

  startClock() {
    setInterval(() => {
      const clockEl = document.getElementById("header-clock");
      if (clockEl) {
        clockEl.textContent = new Date().toLocaleTimeString();
      }
    }, 1000);
  },

  switchPersona(persona) {
    document.querySelectorAll(".persona-btn").forEach((b) => {
      b.classList.toggle("active", b.dataset.persona === persona);
      if (b.dataset.persona === persona) {
        b.style.borderColor = "var(--color-primary)";
        b.style.background = "rgba(56, 189, 248, 0.15)";
      } else {
        b.style.borderColor = "transparent";
        b.style.background = "transparent";
      }
    });
    Store.setPersona(persona);
  },

  async handleInjectScenario() {
    const sel = document.getElementById("scenario-select");
    if (!sel) return;
    const scenarioId = sel.value;

    try {
      const res = await API.injectScenario(scenarioId);
      console.log("Scenario injected successfully:", res);
      alert(`[INCIDENT INJECTED]: ${scenarioId}\n\nAutonomous AI Agents are now processing cross-correlation telemetry.`);
      
      // Auto switch to relevant tab so user sees it in action
      if (scenarioId === "scenario_chiller_overheat") {
        Store.setActiveTab("cross_agent");
      } else if (scenarioId === "scenario_restricted_breach") {
        Store.setActiveTab("cross_agent");
      } else if (scenarioId === "scenario_water_leak") {
        Store.setActiveTab("energy");
      } else if (scenarioId === "scenario_peak_demand_spike") {
        Store.setActiveTab("cost");
      }
    } catch (err) {
      alert("Failed to inject scenario: " + err.message);
    }
  },

  updateHealthScore(score) {
    const el = document.getElementById("header-health-score");
    if (el) {
      el.textContent = `${score}%`;
      el.style.color = score >= 85 ? "var(--color-primary)" : score >= 70 ? "var(--color-warning)" : "var(--color-danger)";
    }
  }
};
