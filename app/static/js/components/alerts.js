/**
 * Central Alert Center Component
 * Unified multi-category alert lifecycle management
 */

const AlertsComponent = {
  currentCategory: "All",
  currentSeverity: "All",
  currentStatus: "All",

  async render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-dim);">Loading Central Alerts...</div>`;

    try {
      const alerts = await API.fetchAlerts({
        category: this.currentCategory,
        severity: this.currentSeverity,
        status: this.currentStatus
      });
      Store.updateAlerts(alerts);

      const activeCount = alerts.filter((a) => a.status === "Active").length;
      const criticalCount = alerts.filter((a) => a.severity === "Critical" && a.status === "Active").length;

      el.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 18px;">
          
          <!-- Header Bar -->
          <div class="glass-panel" style="padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--color-danger);">
                CENTRAL ALERT CENTER • UNIFIED FACILITY INCIDENT MANAGEMENT
              </div>
              <h2 style="font-size: 18px; font-weight: 800; color: #FFF; margin: 2px 0;">
                Facility Alerts & Incident Dispatch
              </h2>
              <p style="font-size: 12px; color: var(--text-muted);">
                Consolidated alerts from Energy, Maintenance, Occupancy, Security, Cost, and Cross-Agent Orchestration.
              </p>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
              <span class="badge ${criticalCount > 0 ? 'badge-critical' : 'badge-healthy'}" style="font-size: 11px;">
                ${criticalCount > 0 ? `🚨 ${criticalCount} Critical Active` : '✓ No Critical Alarms'}
              </span>
              <span class="badge badge-warning" style="font-size: 11px;">
                ${activeCount} Active Total
              </span>
            </div>
          </div>

          <!-- Multi-Filter Toolbar -->
          <div class="glass-panel" style="padding: 12px 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
              <span style="font-size: 11px; color: var(--text-muted); font-weight: 700; text-transform: uppercase;">Category:</span>
              ${["All", "Energy", "Maintenance", "Occupancy", "Security", "Cost"]
                .map(
                  (c) => `
                <button 
                  class="btn ${this.currentCategory === c ? 'btn-primary' : 'btn-outline'}" 
                  style="padding: 3px 8px; font-size: 10px;"
                  onclick="AlertsComponent.setCategory('${c}')"
                >
                  ${c}
                </button>
              `
                )
                .join("")}
            </div>

            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
              <span style="font-size: 11px; color: var(--text-muted); font-weight: 700; text-transform: uppercase;">Severity:</span>
              ${["All", "Critical", "High", "Medium", "Low", "Information"]
                .map(
                  (s) => `
                <button 
                  class="btn ${this.currentSeverity === s ? 'btn-primary' : 'btn-outline'}" 
                  style="padding: 3px 8px; font-size: 10px;"
                  onclick="AlertsComponent.setSeverity('${s}')"
                >
                  ${s}
                </button>
              `
                )
                .join("")}
            </div>

            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 11px; color: var(--text-muted); font-weight: 700; text-transform: uppercase;">Status:</span>
              <select 
                onchange="AlertsComponent.setStatus(this.value)"
                style="background: var(--bg-surface-2); color: #FFF; border: 1px solid var(--border-medium); padding: 4px 8px; border-radius: 4px; font-size: 11px;"
              >
                <option value="All" ${this.currentStatus === 'All' ? 'selected' : ''}>All Statuses</option>
                <option value="Active" ${this.currentStatus === 'Active' ? 'selected' : ''}>Active Only</option>
                <option value="In Progress" ${this.currentStatus === 'In Progress' ? 'selected' : ''}>In Progress</option>
                <option value="Resolved" ${this.currentStatus === 'Resolved' ? 'selected' : ''}>Resolved</option>
              </select>
            </div>
          </div>

          <!-- Alert Stream -->
          <div style="display: flex; flex-direction: column; gap: 12px;">
            ${
              alerts.length === 0
                ? `<div class="glass-panel" style="padding: 40px; text-align: center; color: var(--text-dim);">No alerts matching current filter parameters.</div>`
                : alerts
                    .map(
                      (a) => `
                <div class="glass-panel" style="padding: 16px; border-left: 4px solid ${a.severity === 'Critical' ? '#EF4444' : a.severity === 'High' ? '#F59E0B' : a.severity === 'Medium' ? '#38BDF8' : '#10B981'};">
                  <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;">
                    <div>
                      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                        <span class="badge ${a.severity === 'Critical' ? 'badge-critical' : a.severity === 'High' ? 'badge-warning' : 'badge-good'}" style="font-size: 10px;">
                          ${a.severity}
                        </span>
                        <span class="badge badge-purple" style="font-size: 10px;">
                          ${a.category}
                        </span>
                        <span class="mono" style="font-size: 11px; color: var(--color-primary); font-weight: 700;">
                          ${a.id}
                        </span>
                        <span style="font-size: 11px; color: var(--text-dim);">•</span>
                        <span style="font-size: 11px; color: var(--text-muted);">
                          📍 ${a.location}
                        </span>
                      </div>
                      <h3 style="font-size: 15px; font-weight: 700; color: #FFFFFF;">
                        ${a.title}
                      </h3>
                    </div>

                    <div style="text-align: right;">
                      <span class="badge ${a.status === 'Resolved' ? 'badge-healthy' : a.status === 'In Progress' ? 'badge-good' : 'badge-warning'}">
                        ${a.status}
                      </span>
                      <div class="mono" style="font-size: 10px; color: var(--text-dim); margin-top: 4px;">
                        ${a.timestamp}
                      </div>
                    </div>
                  </div>

                  <p style="font-size: 12px; color: var(--text-muted); line-height: 1.4; margin-bottom: 10px;">
                    ${a.description}
                  </p>

                  <!-- AI Root Cause Explanation -->
                  <div style="background: var(--bg-surface-1); padding: 10px 12px; border-radius: 6px; border: 1px solid var(--border-subtle); margin-bottom: 12px;">
                    <div style="font-size: 10px; text-transform: uppercase; color: var(--color-primary); font-weight: 700; margin-bottom: 2px;">
                      🤖 AI Root-Cause Diagnostic (${a.source_agent})
                    </div>
                    <div style="font-size: 11px; color: var(--text-main);">
                      ${a.ai_explanation}
                    </div>
                  </div>

                  <!-- Recommended Action & Execution Buttons -->
                  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div style="font-size: 11px; color: #6EE7B7; background: rgba(16, 185, 129, 0.1); padding: 4px 10px; border-radius: 4px;">
                      <strong>Recommended Action:</strong> ${a.recommended_action}
                    </div>

                    <div style="display: flex; gap: 8px;">
                      ${
                        a.status === "Active"
                          ? `
                        <button class="btn btn-outline" style="font-size: 11px; padding: 4px 10px;" onclick="AlertsComponent.acknowledge('${a.id}')">
                          Acknowledge
                        </button>
                      `
                          : ""
                      }
                      ${
                        a.status !== "Resolved"
                          ? `
                        <button class="btn btn-primary" style="font-size: 11px; padding: 4px 10px; background: #059669;" onclick="AlertsComponent.resolve('${a.id}')">
                          ✓ Resolve Incident
                        </button>
                      `
                          : `<span style="font-size: 11px; color: var(--color-success); font-weight: 600;">✓ Resolved</span>`
                      }
                    </div>
                  </div>

                </div>
              `
                    )
                    .join("")
            }
          </div>

        </div>
      `;
    } catch (err) {
      el.innerHTML = `<div style="padding: 40px; color: var(--color-danger);">Failed to load alerts: ${err.message}</div>`;
    }
  },

  setCategory(cat) {
    this.currentCategory = cat;
    this.render("main-content-view");
  },

  setSeverity(sev) {
    this.currentSeverity = sev;
    this.render("main-content-view");
  },

  setStatus(stat) {
    this.currentStatus = stat;
    this.render("main-content-view");
  },

  async acknowledge(alertId) {
    try {
      await API.acknowledgeAlert(alertId);
      this.render("main-content-view");
    } catch (err) {
      alert("Failed: " + err.message);
    }
  },

  async resolve(alertId) {
    try {
      await API.resolveAlert(alertId);
      this.render("main-content-view");
    } catch (err) {
      alert("Failed: " + err.message);
    }
  }
};
