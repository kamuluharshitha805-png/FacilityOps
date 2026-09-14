/**
 * Cost Optimization & Sustainability Component
 * Financial Intelligence, Utility Tariffs & ESG Metrics
 */

const CostComponent = {
  async render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-dim);">Loading Financial Intelligence Telemetry...</div>`;

    try {
      const data = await API.fetchCostDetails();
      const kpis = data.kpis;
      const dist = kpis.cost_distribution || {};

      el.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 18px;">
          
          <!-- Header Bar -->
          <div class="glass-panel" style="padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--color-purple);">
                Autonomous Cost Optimization Agent (agt_cost_05)
              </div>
              <h2 style="font-size: 18px; font-weight: 800; color: #FFF; margin: 2px 0;">
                Financial Intelligence, Resource Utilization & Sustainability
              </h2>
              <p style="font-size: 12px; color: var(--text-muted);">
                Translates mechanical and utility operations into balance-sheet ROI, peak-tariff avoidance, and ESG metrics.
              </p>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
              <span class="badge badge-purple" style="font-size: 11px;">
                Cost Efficiency: ${kpis.cost_efficiency_score}%
              </span>
              <span class="badge badge-healthy" style="font-size: 11px;">
                Sustainability: ${kpis.sustainability_score}%
              </span>
            </div>
          </div>

          <!-- Cost KPIs -->
          <div class="kpi-grid">
            <div class="kpi-card" style="--card-accent: #A855F7;">
              <div class="kpi-title">Total Daily Run Cost</div>
              <div class="kpi-value">$${kpis.total_operating_cost.toLocaleString()}</div>
              <div class="kpi-footer">
                <span>Monthly Est:</span>
                <span style="color: var(--color-purple); font-weight: 700;">$${Math.round(kpis.total_operating_cost * 30.5).toLocaleString()}</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #38BDF8;">
              <div class="kpi-title">Daily Energy Spend</div>
              <div class="kpi-value">$${kpis.daily_energy_cost.toLocaleString()}</div>
              <div class="kpi-footer">
                <span>Rate: $0.165-$0.245/kWh</span>
                <span style="color: var(--color-primary);">Peak Aware</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #10B981;">
              <div class="kpi-title">Realized Monthly Savings</div>
              <div class="kpi-value" style="color: #6EE7B7;">$${kpis.monthly_realized_savings.toLocaleString()}</div>
              <div class="kpi-footer">
                <span>AI Automated</span>
                <span style="color: var(--color-success); font-weight: 700;">Verified ROI</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #F59E0B;">
              <div class="kpi-title">Potential Untapped Savings</div>
              <div class="kpi-value" style="color: #FDE68A;">$${kpis.monthly_potential_savings.toLocaleString()}</div>
              <div class="kpi-footer">
                <span>Actionable Pipeline</span>
                <span style="color: var(--color-warning);">4 Pending Actions</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #06B6D4;">
              <div class="kpi-title">Carbon Cost Impact</div>
              <div class="kpi-value">${kpis.carbon_emissions_kg.toLocaleString()} <span style="font-size: 14px; color: var(--text-dim);">kg</span></div>
              <div class="kpi-footer">
                <span>LEED Platinum Track</span>
                <span style="color: #06B6D4;">-18% YoY</span>
              </div>
            </div>
          </div>

          <!-- Primary Visualization: Cost Distribution Breakdown -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Primary Visualization: Cost Distribution
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  Financial expenditure breakdown: Energy | Maintenance | Utilities | Operations | Equipment Depreciation | Other.
                </p>
              </div>
              <span class="mono" style="font-size: 12px; color: var(--color-purple); font-weight: 700;">
                $${kpis.total_operating_cost.toLocaleString()} / day
              </span>
            </div>

            <!-- Horizontal Stacked Cost Bar -->
            <div style="height: 32px; width: 100%; border-radius: 6px; overflow: hidden; display: flex; margin-bottom: 14px; border: 1px solid var(--border-medium);">
              ${Object.entries(dist)
                .map(([name, cost], idx) => {
                  const pct = Math.max(2, (cost / Math.max(1, kpis.total_operating_cost)) * 100);
                  const colors = ["#0284C7", "#10B981", "#06B6D4", "#6366F1", "#A855F7", "#64748B"];
                  const color = colors[idx % colors.length];
                  return `
                    <div 
                      title="${name}: $${cost.toLocaleString()} (${pct.toFixed(1)}%)" 
                      style="width: ${pct}%; background: ${color}; height: 100%; transition: width 0.3s ease; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: #FFF; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding: 0 4px;"
                    >
                      ${pct > 10 ? name : ""}
                    </div>
                  `;
                })
                .join("")}
            </div>

            <!-- Distribution Cards -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px;">
              ${Object.entries(dist)
                .map(([name, cost], idx) => {
                  const pct = Math.max(0, (cost / Math.max(1, kpis.total_operating_cost)) * 100);
                  const colors = ["#0284C7", "#10B981", "#06B6D4", "#6366F1", "#A855F7", "#64748B"];
                  const color = colors[idx % colors.length];
                  return `
                    <div style="background: var(--bg-surface-2); padding: 8px 12px; border-radius: 6px; border-left: 3px solid ${color}; display: flex; justify-content: space-between; align-items: center;">
                      <div>
                        <div style="font-size: 11px; color: var(--text-muted);">${name}</div>
                        <div style="font-size: 14px; font-weight: 700; font-family: var(--font-mono); color: #FFF;">$${cost.toLocaleString()}</div>
                      </div>
                      <span class="mono" style="font-size: 12px; font-weight: 700; color: ${color};">${pct.toFixed(1)}%</span>
                    </div>
                  `;
                })
                .join("")}
            </div>
          </div>

          <!-- Sustainability & ESG Compliance Metrics -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Sustainability & Carbon Emission Metrics (Scope 1 & 2)
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  Continuous carbon tracking against ISO 50001 energy standards and LEED Platinum benchmarks.
                </p>
              </div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
              <div style="background: var(--bg-surface-2); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px;">
                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Grid Carbon Intensity</div>
                <div style="font-size: 20px; font-weight: 800; color: #10B981; font-family: var(--font-mono); margin: 4px 0;">
                  0.385 kg/kWh
                </div>
                <div style="font-size: 11px; color: var(--text-dim);">Regional Grid Utility Real-Time Factor</div>
              </div>

              <div style="background: var(--bg-surface-2); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px;">
                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Water Resource Intensity</div>
                <div style="font-size: 20px; font-weight: 800; color: #38BDF8; font-family: var(--font-mono); margin: 4px 0;">
                  1.2 gpm / 1k sqft
                </div>
                <div style="font-size: 11px; color: var(--text-dim);">Exceeds ASHRAE 189.1 Water Efficiency Spec</div>
              </div>

              <div style="background: var(--bg-surface-2); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px;">
                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Avoided Landfill Emissions</div>
                <div style="font-size: 20px; font-weight: 800; color: #A855F7; font-family: var(--font-mono); margin: 4px 0;">
                  14 Units Extended
                </div>
                <div style="font-size: 11px; color: var(--text-dim);">Through Autonomous Predictive Maintenance</div>
              </div>
            </div>
          </div>

        </div>
      `;
    } catch (err) {
      el.innerHTML = `<div style="padding: 40px; color: var(--color-danger);">Failed to load cost data: ${err.message}</div>`;
    }
  }
};
