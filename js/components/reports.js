/**
 * Automated Facility Reporting Engine Component
 */

const ReportsComponent = {
  currentPeriod: "Last 24 Hours",

  async render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-dim);">Generating Automated Facility Intelligence Report...</div>`;

    try {
      const rep = await API.generateReport(this.currentPeriod);
      const ex = rep.executive_summary;
      const en = rep.energy_intelligence;
      const ma = rep.predictive_maintenance;
      const oc = rep.occupancy_intelligence;
      const sc = rep.security_intelligence;
      const co = rep.cost_optimization;
      const su = rep.sustainability;

      el.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 18px;">
          
          <!-- Report Generation Header & Controls -->
          <div class="glass-panel" style="padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--color-primary);">
                AUTONOMOUS REPORTING ENGINE • MULTI-PILLAR AUDIT GENERATOR
              </div>
              <h2 style="font-size: 18px; font-weight: 800; color: #FFF; margin: 2px 0;">
                Facility Intelligence & Operations Report
              </h2>
              <p style="font-size: 12px; color: var(--text-muted);">
                Consolidated audit report across Energy, Maintenance, Occupancy, Security, Cost, and ESG Sustainability.
              </p>
            </div>
            
            <div style="display: flex; gap: 10px; align-items: center;">
              <select 
                id="report-period-select" 
                onchange="ReportsComponent.changePeriod(this.value)"
                style="background: var(--bg-surface-2); color: #FFF; border: 1px solid var(--border-medium); padding: 6px 10px; border-radius: 6px; font-size: 12px;"
              >
                <option value="Last 24 Hours" ${this.currentPeriod === 'Last 24 Hours' ? 'selected' : ''}>Period: Last 24 Hours</option>
                <option value="Last 7 Days" ${this.currentPeriod === 'Last 7 Days' ? 'selected' : ''}>Period: Last 7 Days</option>
                <option value="Monthly Executive Audit" ${this.currentPeriod === 'Monthly Executive Audit' ? 'selected' : ''}>Period: Monthly Executive Audit</option>
              </select>
              <button class="btn btn-outline" onclick="window.print()">
                🖨️ Print / Save PDF
              </button>
              <button class="btn btn-primary" onclick="ReportsComponent.exportJson('${rep.report_id}')">
                📥 Export JSON
              </button>
            </div>
          </div>

          <!-- Printable Report Container -->
          <div class="glass-panel" style="padding: 30px; background: #0B1120; border: 1px solid #334155;">
            
            <!-- Document Header Banner -->
            <div style="display: flex; justify-content: space-between; border-bottom: 2px solid var(--color-primary); padding-bottom: 16px; margin-bottom: 24px;">
              <div>
                <h1 style="font-size: 22px; font-weight: 800; color: #FFF; letter-spacing: 0.5px;">
                  APEX TOWER GLOBAL HQ
                </h1>
                <div style="font-size: 13px; color: var(--color-primary); font-weight: 600;">
                  ${rep.title}
                </div>
                <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">
                  Generated autonomously on ${rep.generated_at} • Reference: <span class="mono">${rep.report_id}</span>
                </div>
              </div>
              <div style="text-align: right;">
                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Facility Health Index</div>
                <div style="font-size: 32px; font-weight: 900; font-family: var(--font-mono); color: var(--color-primary);">
                  ${rep.facility_health_score}%
                </div>
                <div class="badge badge-healthy">Nominal High</div>
              </div>
            </div>

            <!-- Section 1: Executive Summary -->
            <div style="margin-bottom: 24px;">
              <h3 style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: var(--color-primary); margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
                1. Executive Summary & Core Posture
              </h3>
              <p style="font-size: 13px; color: #F1F5F9; line-height: 1.6; margin-bottom: 12px;">
                ${ex.status_headline}
              </p>
              
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px;">
                <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px;">
                  <div style="font-size: 10px; color: var(--text-muted);">Major Active Issues</div>
                  <div style="font-size: 18px; font-weight: 700; color: #FFF;">${ex.major_issues_count}</div>
                </div>
                <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px;">
                  <div style="font-size: 10px; color: var(--text-muted);">Critical Risks</div>
                  <div style="font-size: 18px; font-weight: 700; color: ${ex.critical_risks_count > 0 ? '#F87171' : '#10B981'};">${ex.critical_risks_count}</div>
                </div>
                <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px;">
                  <div style="font-size: 10px; color: var(--text-muted);">Prevented Failures</div>
                  <div style="font-size: 18px; font-weight: 700; color: #10B981;">${ex.prevented_catastrophic_failures} saves</div>
                </div>
                <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px;">
                  <div style="font-size: 10px; color: var(--text-muted);">Realized Monthly Savings</div>
                  <div style="font-size: 18px; font-weight: 700; color: #38BDF8;">$${ex.realized_monthly_savings_usd.toLocaleString()}</div>
                </div>
              </div>
            </div>

            <!-- Section 2 & 3: Energy & Maintenance -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: var(--color-primary); margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
                  2. Energy & Utilities Intelligence
                </h3>
                <ul style="list-style: none; font-size: 12px; color: var(--text-muted); display: flex; flex-direction: column; gap: 6px;">
                  <li>• Total Energy Consumption: <strong style="color: #FFF;">${en.total_consumption_kwh.toLocaleString()} kWh</strong></li>
                  <li>• Peak Electric Demand: <strong style="color: #FFF;">${en.peak_demand_kw} kW</strong></li>
                  <li>• Water Consumption: <strong style="color: #FFF;">${en.water_consumption_gal.toLocaleString()} gal</strong></li>
                  <li>• Carbon Footprint: <strong style="color: #FFF;">${en.carbon_emissions_kg.toLocaleString()} kg CO₂e</strong></li>
                  <li>• Key Opportunity: <span style="color: #6EE7B7;">${en.key_opportunity}</span></li>
                </ul>
              </div>

              <div>
                <h3 style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: var(--color-primary); margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
                  3. Predictive Maintenance Intelligence
                </h3>
                <ul style="list-style: none; font-size: 12px; color: var(--text-muted); display: flex; flex-direction: column; gap: 6px;">
                  <li>• Total Monitored Assets: <strong style="color: #FFF;">${ma.total_assets_monitored} units</strong></li>
                  <li>• Equipment Health: <strong style="color: #10B981;">${ma.healthy_assets} Healthy</strong> / <strong style="color: #F87171;">${ma.critical_assets} Critical</strong></li>
                  <li>• Mean Time Between Failures: <strong style="color: #FFF;">${ma.mean_time_between_failures_hrs.toLocaleString()} hrs</strong></li>
                  <li>• Active Work Orders: <strong style="color: #FFF;">${ma.open_work_orders_count} open</strong></li>
                  <li>• Asset Focus: <span style="color: #FDE68A;">${ma.critical_asset_focus}</span></li>
                </ul>
              </div>
            </div>

            <!-- Section 4 & 5: Occupancy & Security -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: var(--color-primary); margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
                  4. Occupancy & Spatial Intelligence
                </h3>
                <ul style="list-style: none; font-size: 12px; color: var(--text-muted); display: flex; flex-direction: column; gap: 6px;">
                  <li>• Current Facility Headcount: <strong style="color: #FFF;">${oc.current_headcount} occupants</strong></li>
                  <li>• Occupancy Rate: <strong style="color: #FFF;">${oc.occupancy_rate_pct}%</strong> (Peak: ${oc.peak_occupancy_headcount})</li>
                  <li>• Authorized Visitors: <strong style="color: #FFF;">${oc.visitor_count} badges</strong></li>
                  <li>• Space Utilization Index: <strong style="color: #FFF;">${oc.space_utilization_score}%</strong></li>
                  <li>• Underutilized Wings: <span style="color: #94A3B8;">${oc.underutilized_zones.join(", ")}</span></li>
                </ul>
              </div>

              <div>
                <h3 style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: var(--color-primary); margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
                  5. Security & Perimeter Intelligence
                </h3>
                <ul style="list-style: none; font-size: 12px; color: var(--text-muted); display: flex; flex-direction: column; gap: 6px;">
                  <li>• Access Control Swipes: <strong style="color: #FFF;">${sc.access_events_logged.toLocaleString()} today</strong></li>
                  <li>• Restricted Zone Swipes: <strong style="color: #FFF;">${sc.restricted_zone_swipes} entries</strong></li>
                  <li>• Active Security Alarms: <strong style="color: #FFF;">${sc.active_security_alarms}</strong></li>
                  <li>• Security Compliance Rating: <strong style="color: #10B981;">${sc.security_compliance_score}%</strong></li>
                  <li>• Perimeter Status: <span style="color: #6EE7B7;">${sc.perimeter_status}</span></li>
                </ul>
              </div>
            </div>

            <!-- Section 6 & 7: Cost & Sustainability -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: var(--color-primary); margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
                  6. Cost Optimization & ROI
                </h3>
                <ul style="list-style: none; font-size: 12px; color: var(--text-muted); display: flex; flex-direction: column; gap: 6px;">
                  <li>• Daily Operating Run Cost: <strong style="color: #FFF;">$${co.daily_operating_cost_usd.toLocaleString()}</strong></li>
                  <li>• Projected Monthly Expenditure: <strong style="color: #FFF;">$${co.monthly_projected_spend_usd.toLocaleString()}</strong></li>
                  <li>• Energy Cost Share: <strong style="color: #FFF;">$${co.energy_cost_share.toLocaleString()}</strong></li>
                  <li>• Maintenance Spend: <strong style="color: #FFF;">$${co.maintenance_cost_share.toLocaleString()}</strong></li>
                  <li>• ROI Financial Impact: <span style="color: #E9D5FF;">${co.financial_roi_summary}</span></li>
                </ul>
              </div>

              <div>
                <h3 style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: var(--color-primary); margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
                  7. Sustainability & ESG Compliance
                </h3>
                <ul style="list-style: none; font-size: 12px; color: var(--text-muted); display: flex; flex-direction: column; gap: 6px;">
                  <li>• Scope 2 Grid Carbon: <strong style="color: #10B981;">${su.scope_2_carbon_kg.toLocaleString()} kg CO₂e</strong></li>
                  <li>• Projected Monthly Carbon: <strong style="color: #FFF;">${su.monthly_carbon_tons} metric tons</strong></li>
                  <li>• Water Efficiency Index: <strong style="color: #FFF;">${su.water_utilization_efficiency}</strong></li>
                  <li>• Sustainability Score: <strong style="color: #10B981;">${su.sustainability_index_score}%</strong></li>
                  <li>• ESG Alignment: <span style="color: #6EE7B7;">${su.esg_alignment}</span></li>
                </ul>
              </div>
            </div>

            <!-- Key Prescriptive Recommendations -->
            <div>
              <h3 style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: var(--color-primary); margin-bottom: 10px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
                Top Recommended Actions & Interventions
              </h3>
              <div style="display: flex; flex-direction: column; gap: 8px;">
                ${rep.key_recommendations
                  .map(
                    (rec) => `
                  <div style="background: var(--bg-surface-2); padding: 10px 14px; border-radius: 6px; border-left: 3px solid #38BDF8; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                    <div>
                      <div style="font-size: 12px; font-weight: 700; color: #FFF;">${rec.title}</div>
                      <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">${rec.action}</div>
                    </div>
                    <div style="text-align: right;">
                      <span class="badge ${rec.priority === 'Critical' ? 'badge-critical' : rec.priority === 'High' ? 'badge-warning' : 'badge-good'}">
                        ${rec.priority}
                      </span>
                      ${
                        rec.estimated_savings_usd > 0
                          ? `<div style="font-size: 11px; color: #6EE7B7; font-weight: 700; margin-top: 2px;">+$${rec.estimated_savings_usd.toLocaleString()}/mo</div>`
                          : ""
                      }
                    </div>
                  </div>
                `
                  )
                  .join("")}
              </div>
            </div>

          </div>

        </div>
      `;
    } catch (err) {
      el.innerHTML = `<div style="padding: 40px; color: var(--color-danger);">Failed to generate report: ${err.message}</div>`;
    }
  },

  changePeriod(period) {
    this.currentPeriod = period;
    this.render("main-content-view");
  },

  async exportJson(reportId) {
    try {
      const rep = await API.generateReport(this.currentPeriod);
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(rep, null, 2));
      const downloadAnchor = document.createElement("a");
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", `${reportId}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    } catch (err) {
      alert("Export failed: " + err.message);
    }
  }
};
