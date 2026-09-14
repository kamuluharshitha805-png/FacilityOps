/**
 * Executive Facility Intelligence Command Center
 * "What is happening, why is it happening, what will happen next, and what should we do?"
 */

const ExecutiveComponent = {
  render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    const ov = Store.state.overview;
    if (!ov) {
      el.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-dim);">Connecting to FacilityOps AI Operating System...</div>`;
      return;
    }

    const sub = ov.sub_scores;

    el.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 18px;">
        
        <!-- Executive Intelligence Mission Banner -->
        <div class="glass-panel" style="padding: 16px 20px; background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.6) 100%); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
          <div>
            <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--color-primary); letter-spacing: 0.5px;">
              FACILITY INTELLIGENCE COMMAND CENTER • REAL-TIME OPERATIONAL OS
            </div>
            <h2 style="font-size: 20px; font-weight: 800; color: #FFFFFF; margin: 2px 0;">
              Apex Tower Global Facility Command
            </h2>
            <p style="font-size: 12px; color: var(--text-muted);">
              Autonomous multi-agent correlation active across 5 floors, 24 zones, and 50+ critical industrial assets.
            </p>
          </div>
          <div style="display: flex; gap: 10px;">
            <button class="btn btn-outline" onclick="Store.setActiveTab('cross_agent')">
              ⚡ Inspect Cross-Agent Engine
            </button>
            <button class="btn btn-primary" onclick="Store.setActiveTab('reports')">
              📄 Generate Executive Audit
            </button>
          </div>
        </div>

        <!-- 6-Pillar Health Score Breakdown Grid -->
        <div class="glass-panel" style="padding: 18px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <div>
              <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFFFFF;">
                Unified Facility Health Index
              </h3>
              <p style="font-size: 11px; color: var(--text-muted);">
                Autonomous weighted composite score across all facility operational domains.
              </p>
            </div>
            <div style="display: flex; align-items: baseline; gap: 6px;">
              <span style="font-size: 28px; font-weight: 800; font-family: var(--font-mono); color: var(--color-primary);">
                ${ov.facility_health_score}%
              </span>
              <span class="badge ${ov.facility_health_score >= 85 ? 'badge-healthy' : 'badge-warning'}">
                ${ov.facility_health_score >= 85 ? 'Nominal High' : 'Degraded Warning'}
              </span>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px;">
            <div style="background: var(--bg-surface-2); padding: 10px 12px; border-radius: 6px; border-left: 3px solid #38BDF8;">
              <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Energy (20%)</div>
              <div style="font-size: 18px; font-weight: 700; font-family: var(--font-mono); color: #FFF;">${sub.energy}%</div>
              <div style="font-size: 10px; color: var(--color-primary);">${ov.total_power_kw} kW Active</div>
            </div>
            <div style="background: var(--bg-surface-2); padding: 10px 12px; border-radius: 6px; border-left: 3px solid #10B981;">
              <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Maintenance (25%)</div>
              <div style="font-size: 18px; font-weight: 700; font-family: var(--font-mono); color: #FFF;">${sub.maintenance}%</div>
              <div style="font-size: 10px; color: var(--color-success);">${ov.critical_assets} Critical Assets</div>
            </div>
            <div style="background: var(--bg-surface-2); padding: 10px 12px; border-radius: 6px; border-left: 3px solid #818CF8;">
              <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Occupancy (15%)</div>
              <div style="font-size: 18px; font-weight: 700; font-family: var(--font-mono); color: #FFF;">${sub.occupancy}%</div>
              <div style="font-size: 10px; color: var(--color-accent);">${ov.current_occupancy} People Present</div>
            </div>
            <div style="background: var(--bg-surface-2); padding: 10px 12px; border-radius: 6px; border-left: 3px solid #F59E0B;">
              <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Security (15%)</div>
              <div style="font-size: 18px; font-weight: 700; font-family: var(--font-mono); color: #FFF;">${sub.security}%</div>
              <div style="font-size: 10px; color: var(--color-warning);">${ov.active_security_events_count} Active Events</div>
            </div>
            <div style="background: var(--bg-surface-2); padding: 10px 12px; border-radius: 6px; border-left: 3px solid #A855F7;">
              <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Cost Efficiency (15%)</div>
              <div style="font-size: 18px; font-weight: 700; font-family: var(--font-mono); color: #FFF;">${sub.cost}%</div>
              <div style="font-size: 10px; color: var(--color-purple);">$${ov.daily_operating_cost.toLocaleString()}/day</div>
            </div>
            <div style="background: var(--bg-surface-2); padding: 10px 12px; border-radius: 6px; border-left: 3px solid #14B8A6;">
              <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Sustainability (10%)</div>
              <div style="font-size: 18px; font-weight: 700; font-family: var(--font-mono); color: #FFF;">${sub.sustainability}%</div>
              <div style="font-size: 10px; color: #14B8A6;">${ov.daily_carbon_kg} kg CO₂e</div>
            </div>
          </div>
        </div>

        <!-- High-Impact Operational KPI Grid -->
        <div class="kpi-grid">
          <div class="kpi-card" style="--card-accent: #38BDF8;">
            <div class="kpi-title">Power Demand</div>
            <div class="kpi-value">${ov.total_power_kw} <span style="font-size: 14px; color: var(--text-dim);">kW</span></div>
            <div class="kpi-footer">
              <span>Peak: ${ov.peak_demand_kw} kW</span>
              <span style="color: var(--color-primary);">Daily: ${ov.daily_energy_kwh.toLocaleString()} kWh</span>
            </div>
          </div>

          <div class="kpi-card" style="--card-accent: #10B981;">
            <div class="kpi-title">Equipment Health</div>
            <div class="kpi-value">${ov.healthy_assets + ov.good_assets} <span style="font-size: 14px; color: var(--text-dim);">/ ${ov.total_assets}</span></div>
            <div class="kpi-footer">
              <span>Warning: ${ov.warning_assets}</span>
              <span style="color: ${ov.critical_assets > 0 ? 'var(--color-danger)' : 'var(--color-success)'}; font-weight: 700;">
                Critical: ${ov.critical_assets}
              </span>
            </div>
          </div>

          <div class="kpi-card" style="--card-accent: #818CF8;">
            <div class="kpi-title">Building Occupancy</div>
            <div class="kpi-value">${ov.current_occupancy} <span style="font-size: 14px; color: var(--text-dim);">(${ov.occupancy_rate}%)</span></div>
            <div class="kpi-footer">
              <span>Capacity: 1,600</span>
              <span style="color: var(--color-accent);">Active Zones: 21/24</span>
            </div>
          </div>

          <div class="kpi-card" style="--card-accent: #EF4444;">
            <div class="kpi-title">Active Central Alerts</div>
            <div class="kpi-value" style="color: ${ov.active_alerts_count > 0 ? '#F87171' : '#FFF'};">
              ${ov.active_alerts_count}
            </div>
            <div class="kpi-footer">
              <span>Open WOs: ${ov.open_work_orders_count}</span>
              <span style="color: var(--color-success);">Prevented: ${ov.prevented_failures_count}</span>
            </div>
          </div>

          <div class="kpi-card" style="--card-accent: #A855F7;">
            <div class="kpi-title">Run Cost & Savings</div>
            <div class="kpi-value">$${ov.daily_operating_cost.toLocaleString()}</div>
            <div class="kpi-footer">
              <span>Est. Potential:</span>
              <span style="color: var(--color-purple); font-weight: 700;">+$${ov.estimated_monthly_savings_usd.toLocaleString()}/mo</span>
            </div>
          </div>
        </div>

        <!-- 2-Column Split: Active Cross-Agent Reasoning & Top Priorities -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 16px;">
          
          <!-- Column 1: Live Cross-Agent Synthesis -->
          <div class="glass-panel" style="padding: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span class="beacon-live"></span>
                <h3 style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Active Cross-Agent Correlations
                </h3>
              </div>
              <span class="badge badge-purple">Autonomous Multi-Agent</span>
            </div>

            <div id="exec-correlations-container">
              ${ExecutiveComponent.renderCorrelations()}
            </div>
          </div>

          <!-- Column 2: Top AI Explainable Recommendations -->
          <div class="glass-panel" style="padding: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
              <h3 style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                Top AI Prescriptive Recommendations
              </h3>
              <button class="btn btn-outline" style="font-size: 11px; padding: 2px 8px;" onclick="Store.setActiveTab('insights')">
                View All (${Store.state.insights.length}) →
              </button>
            </div>

            <div id="exec-insights-container">
              ${ExecutiveComponent.renderTopInsights()}
            </div>
          </div>

        </div>

      </div>
    `;
  },

  renderCorrelations() {
    const corrs = Store.state.correlations || [];
    if (corrs.length === 0) {
      return `<p style="color: var(--text-dim); font-size: 12px; padding: 20px 0;">All agent telemetry running nominal with no inter-agent anomaly correlations detected.</p>`;
    }

    return corrs
      .slice(0, 3)
      .map(
        (c) => `
      <div style="background: var(--bg-surface-2); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <span class="badge badge-purple" style="font-size: 10px;">${c.pair}</span>
          <span class="mono" style="font-size: 11px; color: var(--color-primary); font-weight: 700;">${c.confidence_pct}% Match</span>
        </div>
        <div style="font-size: 12px; font-weight: 600; color: #F8FAFC; margin-bottom: 4px;">
          ${c.correlation_rule}
        </div>
        <p style="font-size: 11px; color: var(--text-muted); line-height: 1.4; margin-bottom: 6px;">
          ${c.ai_reasoning}
        </p>
        <div style="font-size: 11px; color: #6EE7B7; background: rgba(16, 185, 129, 0.1); padding: 4px 8px; border-radius: 4px;">
          <strong>Unified Action:</strong> ${c.recommended_unified_action}
        </div>
      </div>
    `
      )
      .join("");
  },

  renderTopInsights() {
    const insights = Store.state.insights || [];
    if (insights.length === 0) {
      return `<p style="color: var(--text-dim); font-size: 12px;">Generating AI insights...</p>`;
    }

    return insights
      .slice(0, 2)
      .map(
        (ins) => `
      <div class="insight-card" style="margin-bottom: 10px; padding: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <span class="badge ${ins.priority === 'Critical' ? 'badge-critical' : ins.priority === 'High' ? 'badge-warning' : 'badge-good'}">
            ${ins.priority} Priority
          </span>
          <span style="font-size: 11px; color: var(--color-primary); font-weight: 700;">
            ${ins.estimated_savings_usd > 0 ? `Save $${ins.estimated_savings_usd.toLocaleString()}/mo` : ins.category}
          </span>
        </div>
        <div style="font-size: 13px; font-weight: 700; color: #FFF; margin-bottom: 4px;">
          ${ins.title}
        </div>
        <p style="font-size: 11px; color: var(--text-muted); line-height: 1.4; margin-bottom: 8px;">
          ${ins.insight}
        </p>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 10px; color: var(--text-dim);">Source: ${ins.agent_source}</span>
          <button class="btn btn-primary" style="padding: 4px 10px; font-size: 11px;" onclick="ExecutiveComponent.executeAction('${ins.id}')">
            ⚡ ${ins.action_label}
          </button>
        </div>
      </div>
    `
      )
      .join("");
  },

  async executeAction(insightId) {
    try {
      await API.executeRecommendation(insightId);
      alert("AI Prescriptive action executed. Building telemetry and equipment status updated.");
      // Refresh
      const [overview, insights, alerts, wos] = await Promise.all([
        API.fetchOverview(),
        API.fetchInsights(),
        API.fetchAlerts(),
        API.fetchWorkOrders()
      ]);
      Store.updateOverview(overview);
      Store.updateInsights(insights);
      Store.updateAlerts(alerts);
      Store.updateWorkOrders(wos);
      this.render("main-content-view");
    } catch (err) {
      alert("Action failed: " + err.message);
    }
  }
};
