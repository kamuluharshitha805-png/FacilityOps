/**
 * Predictive Maintenance Intelligence Component
 * Monitor → Detect → Predict → Prioritize → Schedule → Track
 */

const MaintenanceComponent = {
  async render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-dim);">Loading Predictive Maintenance Telemetry...</div>`;

    try {
      const data = await API.fetchMaintenanceDetails();
      const assets = await API.fetchAssets();
      const kpis = data.kpis;
      const wos = kpis.work_orders || [];
      const calendar = kpis.calendar_events || [];
      const dist = kpis.health_distribution || { healthy: 38, good: 10, warning: 2, critical: 1 };

      el.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 18px;">
          
          <!-- Maintenance Header Bar -->
          <div class="glass-panel" style="padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--color-primary);">
                Autonomous Predictive Maintenance Agent (agt_maint_02)
              </div>
              <h2 style="font-size: 18px; font-weight: 800; color: #FFF; margin: 2px 0;">
                Asset Health, Vibration Telemetry & Failure Risk Forecast
              </h2>
              <p style="font-size: 12px; color: var(--text-muted);">
                Transitions operations from reactive breakdown firefighting to autonomous condition-based prediction.
              </p>
            </div>
            <div style="display: flex; gap: 10px;">
              <button class="btn btn-primary" onclick="MaintenanceComponent.showCreateWoModal()">
                + Create Work Order
              </button>
            </div>
          </div>

          <!-- Maintenance KPIs -->
          <div class="kpi-grid">
            <div class="kpi-card" style="--card-accent: #10B981;">
              <div class="kpi-title">Average Equipment Health</div>
              <div class="kpi-value">${kpis.average_equipment_health}%</div>
              <div class="kpi-footer">
                <span>Total Assets: ${kpis.total_assets}</span>
                <span style="color: var(--color-success);">Healthy: ${kpis.healthy_assets}</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #EF4444;">
              <div class="kpi-title">Critical & Warning Assets</div>
              <div class="kpi-value" style="color: ${kpis.critical_assets > 0 ? 'var(--color-danger)' : 'var(--color-success)'};">
                ${kpis.critical_assets} <span style="font-size: 14px; color: var(--text-dim);">Crit / ${kpis.warning_assets} Warn</span>
              </div>
              <div class="kpi-footer">
                <span>Failure Risk:</span>
                <span style="color: ${kpis.critical_assets > 0 ? 'var(--color-danger)' : 'var(--color-primary)'}; font-weight: 700;">
                  ${kpis.critical_assets > 0 ? 'High (>75%)' : 'Nominal (<10%)'}
                </span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #38BDF8;">
              <div class="kpi-title">Reliability (MTBF)</div>
              <div class="kpi-value">${kpis.mtbf_hours.toLocaleString()} <span style="font-size: 14px; color: var(--text-dim);">hrs</span></div>
              <div class="kpi-footer">
                <span>MTTR: ${kpis.mttr_hours} hrs</span>
                <span style="color: var(--color-primary);">Reliability: 99.4%</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #A855F7;">
              <div class="kpi-title">Prevented Failures</div>
              <div class="kpi-value" style="color: #E9D5FF;">${kpis.prevented_failures}</div>
              <div class="kpi-footer">
                <span>Catastrophic Saves</span>
                <span style="color: var(--color-purple); font-weight: 700;">$240k+ Capital Avoided</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #F59E0B;">
              <div class="kpi-title">Work Orders Status</div>
              <div class="kpi-value">${kpis.open_work_orders} <span style="font-size: 14px; color: var(--text-dim);">Open</span></div>
              <div class="kpi-footer">
                <span>Completed: ${kpis.completed_work_orders}</span>
                <span style="color: var(--color-warning);">YTD: $${kpis.maintenance_cost_ytd.toLocaleString()}</span>
              </div>
            </div>
          </div>

          <!-- Primary Visualization: Equipment Health Distribution -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Primary Visualization: Equipment Health Distribution
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  Categorized asset condition scores: Healthy (>85%), Good (70-85%), Warning (50-69%), Critical (<50%).
                </p>
              </div>
              <span class="mono" style="font-size: 12px; color: var(--color-primary); font-weight: 700;">
                ${kpis.total_assets} Monitored Units
              </span>
            </div>

            <!-- Health Bar Distribution -->
            <div style="height: 32px; width: 100%; border-radius: 6px; overflow: hidden; display: flex; margin-bottom: 14px; border: 1px solid var(--border-medium);">
              <div style="width: ${(dist.healthy / kpis.total_assets) * 100}%; background: #10B981; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #FFF;">
                ${dist.healthy} Healthy
              </div>
              <div style="width: ${(dist.good / kpis.total_assets) * 100}%; background: #38BDF8; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #FFF;">
                ${dist.good} Good
              </div>
              ${
                dist.warning > 0
                  ? `
                <div style="width: ${(dist.warning / kpis.total_assets) * 100}%; background: #F59E0B; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #FFF;">
                  ${dist.warning} Warn
                </div>
              `
                  : ""
              }
              ${
                dist.critical > 0
                  ? `
                <div style="width: ${(dist.critical / kpis.total_assets) * 100}%; background: #EF4444; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #FFF;" class="beacon-critical">
                  ${dist.critical} Crit
                </div>
              `
                  : ""
              }
            </div>

            <!-- Distribution Cards -->
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
              <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px; border-left: 3px solid #10B981;">
                <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Healthy (>85%)</div>
                <div style="font-size: 18px; font-weight: 700; color: #10B981;">${dist.healthy} Units</div>
              </div>
              <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px; border-left: 3px solid #38BDF8;">
                <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Good (70-85%)</div>
                <div style="font-size: 18px; font-weight: 700; color: #38BDF8;">${dist.good} Units</div>
              </div>
              <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px; border-left: 3px solid #F59E0B;">
                <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Warning (50-69%)</div>
                <div style="font-size: 18px; font-weight: 700; color: #F59E0B;">${dist.warning} Units</div>
              </div>
              <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px; border-left: 3px solid #EF4444;">
                <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Critical (<50%)</div>
                <div style="font-size: 18px; font-weight: 700; color: #EF4444;">${dist.critical} Units</div>
              </div>
            </div>
          </div>

          <!-- Predictive Work Orders Tracking Table -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Predictive Maintenance Work Orders & Execution Lifecycle
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  Track dispatched corrective actions triggered autonomously by AI vibration and thermal telemetry.
                </p>
              </div>
            </div>

            <div class="table-container">
              <table class="facility-table">
                <thead>
                  <tr>
                    <th>WO ID</th>
                    <th>Asset Tag & Name</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Assigned Team / Tech</th>
                    <th>AI Trigger Reason</th>
                    <th>Est. Cost</th>
                    <th>Lifecycle Action</th>
                  </tr>
                </thead>
                <tbody>
                  ${wos
                    .map(
                      (wo) => `
                    <tr>
                      <td class="mono" style="font-weight: 700; color: var(--color-primary);">${wo.id}</td>
                      <td>
                        <div style="font-weight: 600;">${wo.asset_name}</div>
                        <div style="font-size: 10px; color: var(--text-dim);">${wo.location}</div>
                      </td>
                      <td>
                        <span class="badge ${wo.priority === 'Critical' ? 'badge-critical' : wo.priority === 'High' ? 'badge-warning' : 'badge-good'}">
                          ${wo.priority}
                        </span>
                      </td>
                      <td>
                        <span class="badge ${wo.status === 'Completed' ? 'badge-healthy' : wo.status === 'In Progress' ? 'badge-good' : 'badge-warning'}">
                          ${wo.status}
                        </span>
                      </td>
                      <td style="font-size: 11px;">${wo.assigned_to}</td>
                      <td style="font-size: 11px; color: var(--text-muted); max-width: 250px;">${wo.ai_trigger_reason}</td>
                      <td class="mono" style="font-weight: 700;">$${wo.estimated_cost_usd}</td>
                      <td>
                        ${
                          wo.status !== "Completed"
                            ? `
                          <div style="display: flex; gap: 4px;">
                            ${
                              wo.status !== "In Progress"
                                ? `<button class="btn btn-outline" style="padding: 2px 6px; font-size: 10px;" onclick="MaintenanceComponent.updateWoStatus('${wo.id}', 'In Progress')">Start</button>`
                                : ""
                            }
                            <button class="btn btn-primary" style="padding: 2px 6px; font-size: 10px; background: #059669;" onclick="MaintenanceComponent.updateWoStatus('${wo.id}', 'Completed')">Complete</button>
                          </div>
                        `
                            : `<span style="font-size: 11px; color: var(--color-success);">✓ Done (${wo.completed_date || 'Today'})</span>`
                        }
                      </td>
                    </tr>
                  `
                    )
                    .join("")}
                </tbody>
              </table>
            </div>
          </div>

          <!-- Interactive Maintenance Schedule Calendar -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Interactive Maintenance Schedule Calendar
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  Forward-looking condition-based service windows scheduled around low-occupancy facility envelopes.
                </p>
              </div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
              ${calendar
                .map(
                  (evt) => `
                <div style="background: var(--bg-surface-2); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span class="mono" style="font-size: 11px; color: var(--color-primary); font-weight: 700;">${evt.date}</span>
                    <span class="badge ${evt.priority === 'Critical' ? 'badge-critical' : evt.priority === 'High' ? 'badge-warning' : 'badge-good'}" style="font-size: 9px;">
                      ${evt.priority}
                    </span>
                  </div>
                  <div style="font-size: 12px; font-weight: 700; color: #FFF; margin-bottom: 4px;">${evt.title}</div>
                  <div style="font-size: 11px; color: var(--text-dim); display: flex; justify-content: space-between;">
                    <span>Asset: ${evt.asset}</span>
                    <span style="color: var(--color-accent);">${evt.type}</span>
                  </div>
                </div>
              `
                )
                .join("")}
            </div>
          </div>

          <!-- All Critical Asset Telemetry Table -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                Real-Time Asset Condition Telemetry (${assets.length} Units)
              </h3>
            </div>

            <div class="table-container">
              <table class="facility-table">
                <thead>
                  <tr>
                    <th>Tag</th>
                    <th>Asset Name</th>
                    <th>Type</th>
                    <th>Health Score</th>
                    <th>Failure Probability</th>
                    <th>RUL Indicator</th>
                    <th>Vibration RMS</th>
                    <th>Temperature</th>
                    <th>Why / Contributing Factors</th>
                  </tr>
                </thead>
                <tbody>
                  ${assets
                    .map(
                      (a) => `
                    <tr>
                      <td class="mono" style="font-weight: 700; color: var(--color-primary);">${a.id}</td>
                      <td>
                        <div style="font-weight: 600;">${a.name}</div>
                        <div style="font-size: 10px; color: var(--text-dim);">Zone: ${a.zone_id} | Crit: ${a.criticality}</div>
                      </td>
                      <td>${a.type}</td>
                      <td>
                        <span class="badge ${a.health_score >= 85 ? 'badge-healthy' : a.health_score >= 70 ? 'badge-good' : a.health_score >= 50 ? 'badge-warning' : 'badge-critical'}">
                          ${a.health_score}% (${a.health_status})
                        </span>
                      </td>
                      <td class="mono" style="color: ${a.failure_probability_pct > 50 ? 'var(--color-danger)' : 'var(--text-main)'}; font-weight: 700;">
                        ${a.failure_probability_pct}%
                      </td>
                      <td class="mono" style="font-size: 11px;">${Math.round(a.rul_hours).toLocaleString()} hrs</td>
                      <td class="mono" style="color: ${a.vibration_rms > a.baseline_vibration * 1.5 ? 'var(--color-danger)' : 'var(--text-main)'};">
                        ${a.vibration_rms} mm/s
                      </td>
                      <td class="mono">${a.temperature_c}°C</td>
                      <td style="font-size: 11px; color: var(--text-muted); max-width: 240px;">
                        ${a.contributing_factors ? a.contributing_factors.join(", ") : 'Nominal'}
                      </td>
                    </tr>
                  `
                    )
                    .join("")}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      `;
    } catch (err) {
      el.innerHTML = `<div style="padding: 40px; color: var(--color-danger);">Failed to load maintenance data: ${err.message}</div>`;
    }
  },

  async updateWoStatus(woId, status) {
    try {
      await API.updateWorkOrderStatus(woId, status);
      this.render("main-content-view");
    } catch (err) {
      alert("Failed to update status: " + err.message);
    }
  },

  showCreateWoModal() {
    const modalHtml = `
      <div class="modal-backdrop" id="create-wo-modal">
        <div class="modal-content">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <h3 style="font-size: 18px; color: #FFF;">+ Create Predictive Work Order</h3>
            <button class="btn btn-outline" onclick="document.getElementById('create-wo-modal').remove()">✕</button>
          </div>
          <form onsubmit="MaintenanceComponent.handleCreateWo(event)" style="display: flex; flex-direction: column; gap: 12px;">
            <div>
              <label style="display: block; font-size: 11px; color: var(--text-muted); margin-bottom: 4px;">Target Asset</label>
              <select id="wo-asset-select" style="width: 100%; background: var(--bg-surface-2); color: #FFF; border: 1px solid var(--border-medium); padding: 8px; border-radius: 4px;">
                <option value="CH-02|Centrifugal Water Chiller 2|Floor 5 Mechanical Penthouse">CH-02 - Centrifugal Water Chiller 2 (Penthouse)</option>
                <option value="AHU-F2-01|Floor 2 Labs Clean Supply AHU|Floor 2 Cleanroom Plant">AHU-F2-01 - Floor 2 Labs Clean Supply AHU</option>
                <option value="PMP-03|Condenser Water Pump 1|Floor 5 Mechanical Room">PMP-03 - Condenser Water Pump 1</option>
                <option value="CRAC-02|Mission Data Center CRAC 2|Floor 5 Data Center Alpha">CRAC-02 - Mission Data Center CRAC 2</option>
                <option value="ELV-01|High-Speed Passenger Elevator 1|Floor 1 Atrium">ELV-01 - Passenger Elevator 1</option>
              </select>
            </div>
            <div>
              <label style="display: block; font-size: 11px; color: var(--text-muted); margin-bottom: 4px;">Work Order Title</label>
              <input id="wo-title" type="text" required value="Vibration Harmonic Analysis & Coupling Rebalance" style="width: 100%; background: var(--bg-surface-2); color: #FFF; border: 1px solid var(--border-medium); padding: 8px; border-radius: 4px;" />
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
              <div>
                <label style="display: block; font-size: 11px; color: var(--text-muted); margin-bottom: 4px;">Priority</label>
                <select id="wo-priority" style="width: 100%; background: var(--bg-surface-2); color: #FFF; border: 1px solid var(--border-medium); padding: 8px; border-radius: 4px;">
                  <option value="Critical">Critical</option>
                  <option value="High" selected>High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
              </div>
              <div>
                <label style="display: block; font-size: 11px; color: var(--text-muted); margin-bottom: 4px;">Assigned Specialist</label>
                <input id="wo-assigned" type="text" value="Mechanical Lead - Mark Vance" style="width: 100%; background: var(--bg-surface-2); color: #FFF; border: 1px solid var(--border-medium); padding: 8px; border-radius: 4px;" />
              </div>
            </div>
            <div>
              <label style="display: block; font-size: 11px; color: var(--text-muted); margin-bottom: 4px;">Maintenance Action Description</label>
              <textarea id="wo-action" rows="3" style="width: 100%; background: var(--bg-surface-2); color: #FFF; border: 1px solid var(--border-medium); padding: 8px; border-radius: 4px;">Perform laser shaft alignment, verify oil lubricity, and re-torque mounting bolts.</textarea>
            </div>
            <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 10px;">
              <button type="button" class="btn btn-outline" onclick="document.getElementById('create-wo-modal').remove()">Cancel</button>
              <button type="submit" class="btn btn-primary">Dispatch Work Order</button>
            </div>
          </form>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML("beforeend", modalHtml);
  },

  async handleCreateWo(event) {
    event.preventDefault();
    const assetRaw = document.getElementById("wo-asset-select").value.split("|");
    const payload = {
      asset_id: assetRaw[0],
      asset_name: assetRaw[1],
      location: assetRaw[2],
      title: document.getElementById("wo-title").value,
      priority: document.getElementById("wo-priority").value,
      assigned_to: document.getElementById("wo-assigned").value,
      team: "Mechanical",
      estimated_hours: 3.5,
      estimated_cost_usd: 850.0,
      maintenance_action: document.getElementById("wo-action").value,
      ai_trigger_reason: "Manual dispatch via FacilityOps Work Order Command interface."
    };

    try {
      await API.createWorkOrder(payload);
      document.getElementById("create-wo-modal").remove();
      alert("Work order created and dispatched to maintenance team queue.");
      this.render("main-content-view");
    } catch (err) {
      alert("Error: " + err.message);
    }
  }
};
