/**
 * Energy Intelligence & Monitoring Component
 */

const EnergyComponent = {
  async render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-dim);">Loading Energy Intelligence Telemetry...</div>`;

    try {
      const data = await API.fetchEnergyDetails();
      const kpis = data.kpis;
      const hourly = data.hourly_history || [];
      const dist = kpis.energy_distribution || {};

      el.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 18px;">
          
          <!-- Energy Header Bar -->
          <div class="glass-panel" style="padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--color-primary);">
                Autonomous Energy Intelligence Agent (agt_energy_01)
              </div>
              <h2 style="font-size: 18px; font-weight: 800; color: #FFF; margin: 2px 0;">
                Utility, Smart Metering & Carbon Tracking
              </h2>
              <p style="font-size: 12px; color: var(--text-muted);">
                Continuously optimizes power demand, water consumption, HVAC efficiency, and tariff peak shaving.
              </p>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
              <span class="badge ${kpis.energy_efficiency_score >= 80 ? 'badge-healthy' : 'badge-warning'}">
                Efficiency: ${kpis.energy_efficiency_score}%
              </span>
              <button class="btn btn-outline" onclick="Store.setActiveTab('occupancy'); Store.setHeatmapMetric('energy');">
                🗺️ View Energy Heatmap
              </button>
            </div>
          </div>

          <!-- Energy High-Visibility KPIs -->
          <div class="kpi-grid">
            <div class="kpi-card" style="--card-accent: #38BDF8;">
              <div class="kpi-title">Current Power Demand</div>
              <div class="kpi-value">${kpis.total_power_kw} <span style="font-size: 14px; color: var(--text-dim);">kW</span></div>
              <div class="kpi-footer">
                <span>Peak: ${kpis.peak_demand_kw} kW</span>
                <span style="color: var(--color-primary);">Daily: ${kpis.daily_energy_kwh.toLocaleString()} kWh</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #0EA5E9;">
              <div class="kpi-title">HVAC Consumption</div>
              <div class="kpi-value">${kpis.hvac_energy_kw} <span style="font-size: 14px; color: var(--text-dim);">kW</span></div>
              <div class="kpi-footer">
                <span>Share: ${roundVal((kpis.hvac_energy_kw / maxVal(1, kpis.total_power_kw)) * 100)}%</span>
                <span style="color: var(--color-success);">COP Avg: 4.8</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #06B6D4;">
              <div class="kpi-title">Water Consumption</div>
              <div class="kpi-value">${kpis.water_flow_gpm} <span style="font-size: 14px; color: var(--text-dim);">GPM</span></div>
              <div class="kpi-footer">
                <span>Daily: ${kpis.daily_water_gal.toLocaleString()} gal</span>
                <span style="color: ${kpis.water_flow_gpm > 60 ? 'var(--color-danger)' : 'var(--color-primary)'}; font-weight: 600;">
                  ${kpis.water_flow_gpm > 60 ? '⚠️ High Leak Risk' : 'Nominal Flow'}
                </span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #10B981;">
              <div class="kpi-title">Carbon Footprint</div>
              <div class="kpi-value">${kpis.daily_carbon_kg.toLocaleString()} <span style="font-size: 14px; color: var(--text-dim);">kg</span></div>
              <div class="kpi-footer">
                <span>Scope 2 Grid</span>
                <span style="color: #10B981;">0.385 kg/kWh</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #A855F7;">
              <div class="kpi-title">Energy Savings ROI</div>
              <div class="kpi-value" style="color: #E9D5FF;">$${kpis.potential_savings_usd.toLocaleString()}</div>
              <div class="kpi-footer">
                <span>Realized: $${kpis.realized_savings_usd.toLocaleString()}</span>
                <span style="color: var(--color-purple); font-weight: 700;">Potential / Mo</span>
              </div>
            </div>
          </div>

          <!-- Primary Visualization: Energy Distribution Breakdown -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Primary Visualization: Energy Distribution (kW Load Profile)
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  Real-time power allocation across mechanical, lighting, IT computing, and peripheral utilities.
                </p>
              </div>
              <span class="mono" style="font-size: 12px; color: var(--color-primary); font-weight: 700;">
                Total: ${kpis.total_power_kw} kW
              </span>
            </div>

            <!-- Horizontal Stacked Distribution Bar -->
            <div style="height: 32px; width: 100%; border-radius: 6px; overflow: hidden; display: flex; margin-bottom: 14px; border: 1px solid var(--border-medium);">
              ${Object.entries(dist)
                .map(([name, kw], idx) => {
                  const pct = Math.max(2, (kw / Math.max(1, kpis.total_power_kw)) * 100);
                  const colors = ["#0284C7", "#38BDF8", "#818CF8", "#A855F7", "#64748B"];
                  const color = colors[idx % colors.length];
                  return `
                    <div 
                      title="${name}: ${kw} kW (${pct.toFixed(1)}%)" 
                      style="width: ${pct}%; background: ${color}; height: 100%; transition: width 0.3s ease; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: #FFF; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding: 0 4px;"
                    >
                      ${pct > 8 ? name : ""}
                    </div>
                  `;
                })
                .join("")}
            </div>

            <!-- Legend Grid -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px;">
              ${Object.entries(dist)
                .map(([name, kw], idx) => {
                  const pct = Math.max(0, (kw / Math.max(1, kpis.total_power_kw)) * 100);
                  const colors = ["#0284C7", "#38BDF8", "#818CF8", "#A855F7", "#64748B"];
                  const color = colors[idx % colors.length];
                  return `
                    <div style="background: var(--bg-surface-2); padding: 8px 12px; border-radius: 6px; border-left: 3px solid ${color}; display: flex; justify-content: space-between; align-items: center;">
                      <div>
                        <div style="font-size: 11px; color: var(--text-muted);">${name}</div>
                        <div style="font-size: 14px; font-weight: 700; font-family: var(--font-mono); color: #FFF;">${kw} kW</div>
                      </div>
                      <span class="mono" style="font-size: 12px; font-weight: 700; color: ${color};">${pct.toFixed(1)}%</span>
                    </div>
                  `;
                })
                .join("")}
            </div>
          </div>

          <!-- Hourly Load Profile & Anomaly Analytics Table -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Electricity & Water Hourly Analytics (24-Hour Horizon)
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  Granular feeder telemetry capturing diurnal ramps, peak demand windows, and water flow trends.
                </p>
              </div>
            </div>

            <div class="table-container">
              <table class="facility-table">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Total Demand</th>
                    <th>HVAC Load</th>
                    <th>Lighting</th>
                    <th>Equipment</th>
                    <th>Water Flow</th>
                    <th>Carbon Output</th>
                    <th>Tariff Period</th>
                  </tr>
                </thead>
                <tbody>
                  ${hourly
                    .slice(-8)
                    .reverse()
                    .map((pt) => {
                      const hr = parseInt(pt.time.split(":")[0], 10);
                      const isPeak = hr >= 12 && hr <= 18;
                      return `
                        <tr>
                          <td class="mono" style="font-weight: 700; color: var(--color-primary);">${pt.time}</td>
                          <td class="mono" style="font-weight: 700;">${pt.total_kw} kW</td>
                          <td class="mono">${pt.hvac_kw} kW</td>
                          <td class="mono">${pt.lighting_kw} kW</td>
                          <td class="mono">${pt.equipment_kw} kW</td>
                          <td class="mono">${pt.water_gpm} GPM</td>
                          <td class="mono">${pt.carbon_kg} kg</td>
                          <td>
                            <span class="badge ${isPeak ? 'badge-critical' : 'badge-good'}">
                              ${isPeak ? 'Peak Tariff ($0.245)' : 'Standard / Off-Peak'}
                            </span>
                          </td>
                        </tr>
                      `;
                    })
                    .join("")}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      `;
    } catch (err) {
      el.innerHTML = `<div style="padding: 40px; color: var(--color-danger);">Failed to load energy data: ${err.message}</div>`;
    }
  }
};

function roundVal(v) {
  return Math.round(v * 10) / 10;
}
function maxVal(a, b) {
  return Math.max(a, b);
}
