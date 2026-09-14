/**
 * Security Intelligence Component
 * Access Control Monitoring, CCTV AI Metadata & Perimeter Defense
 */

const SecurityComponent = {
  async render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-dim);">Loading Security Intelligence Telemetry...</div>`;

    try {
      const data = await API.fetchSecurityDetails();
      const kpis = data.kpis;
      const logs = kpis.recent_access_logs || [];
      const cctv = kpis.cctv_events || [];
      const zones = kpis.zone_activity || {};

      el.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 18px;">
          
          <!-- Header Bar -->
          <div class="glass-panel" style="padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--color-primary);">
                Autonomous Security Intelligence Agent (agt_security_04)
              </div>
              <h2 style="font-size: 18px; font-weight: 800; color: #FFF; margin: 2px 0;">
                Access Control, CCTV Metadata & Perimeter Security
              </h2>
              <p style="font-size: 12px; color: var(--text-muted);">
                Integrates physical badge turnstiles, biometric mantraps, and AI computer vision event telemetry.
              </p>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
              <span class="badge ${kpis.security_health_score >= 90 ? 'badge-healthy' : 'badge-warning'}">
                Security Score: ${kpis.security_health_score}%
              </span>
              <button class="btn btn-primary" onclick="SecurityComponent.simulateBadgeSwipe()">
                💳 Simulate Badge Swipe
              </button>
            </div>
          </div>

          <!-- Security KPIs -->
          <div class="kpi-grid">
            <div class="kpi-card" style="--card-accent: #38BDF8;">
              <div class="kpi-title">Access Swipes Today</div>
              <div class="kpi-value">${kpis.access_events_today.toLocaleString()}</div>
              <div class="kpi-footer">
                <span>Electronic Portals</span>
                <span style="color: var(--color-primary);">99.2% Granted</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #EF4444;">
              <div class="kpi-title">Active Security Alarms</div>
              <div class="kpi-value" style="color: ${kpis.active_security_events > 0 ? 'var(--color-danger)' : 'var(--color-success)'};">
                ${kpis.active_security_events}
              </div>
              <div class="kpi-footer">
                <span>Critical Incidents: ${kpis.critical_incidents_count}</span>
                <span style="color: ${kpis.active_security_events > 0 ? 'var(--color-danger)' : 'var(--color-success)'}; font-weight: 700;">
                  ${kpis.active_security_events > 0 ? 'Action Required' : 'All Clear'}
                </span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #F59E0B;">
              <div class="kpi-title">Restricted-Zone Swipes</div>
              <div class="kpi-value">${kpis.restricted_zone_events_today}</div>
              <div class="kpi-footer">
                <span>Data Center & Labs</span>
                <span style="color: var(--color-warning);">Biometric Verified</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #818CF8;">
              <div class="kpi-title">CCTV AI Vision Events</div>
              <div class="kpi-value">${cctv.length} <span style="font-size: 14px; color: var(--text-dim);">Logged</span></div>
              <div class="kpi-footer">
                <span>PTZ Tracking</span>
                <span style="color: var(--color-accent);">100% Perimeter Coverage</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #10B981;">
              <div class="kpi-title">Perimeter Health</div>
              <div class="kpi-value">${kpis.security_health_score}%</div>
              <div class="kpi-footer">
                <span>Compliance</span>
                <span style="color: var(--color-success);">ISO 27001 Physical</span>
              </div>
            </div>
          </div>

          <!-- Building Zone Security Classification Grid -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Building Zone Security Classifications & Access Policy
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  Enforces defense-in-depth across public atriums, employee operations, restricted labs, and mission-critical server rooms.
                </p>
              </div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">
              <div style="background: var(--bg-surface-2); padding: 12px; border-radius: 8px; border-left: 3px solid #38BDF8;">
                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Public Zones</div>
                <div style="font-size: 18px; font-weight: 700; color: #38BDF8;">${zones.public_zones || 4} Zones</div>
                <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">Main Atrium, Cafeteria, Auditorium</div>
              </div>
              <div style="background: var(--bg-surface-2); padding: 12px; border-radius: 8px; border-left: 3px solid #A855F7;">
                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Operational Zones</div>
                <div style="font-size: 18px; font-weight: 700; color: #A855F7;">${zones.operational_zones || 7} Zones</div>
                <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">Open Workspaces, Collaborative Labs</div>
              </div>
              <div style="background: var(--bg-surface-2); padding: 12px; border-radius: 8px; border-left: 3px solid #F59E0B;">
                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Restricted Zones</div>
                <div style="font-size: 18px; font-weight: 700; color: #F59E0B;">${zones.restricted_zones || 8} Zones</div>
                <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">R&D Hardware, Executive Suite, Chiller Plant</div>
              </div>
              <div style="background: var(--bg-surface-2); padding: 12px; border-radius: 8px; border-left: 3px solid #EF4444;">
                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">High-Security Zones</div>
                <div style="font-size: 18px; font-weight: 700; color: #EF4444;">${zones.high_security_zones || 5} Zones</div>
                <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">Tier-4 Data Center, Substation, Cleanroom</div>
              </div>
            </div>
          </div>

          <!-- 2-Column Live Logs: Access Badge Portals & CCTV Metadata Stream -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 16px;">
            
            <!-- Column 1: Live Access Control Logs -->
            <div class="glass-panel" style="padding: 16px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h3 style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Access Control Swipe Feed
                </h3>
                <span class="badge badge-good">Real-Time</span>
              </div>

              <div class="table-container">
                <table class="facility-table">
                  <thead>
                    <tr>
                      <th>Time</th>
                      <th>User & Role</th>
                      <th>Target Zone</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${logs
                      .map(
                        (l) => `
                      <tr>
                        <td class="mono" style="color: var(--color-primary); font-weight: 700;">${l.timestamp}</td>
                        <td>
                          <div style="font-weight: 600;">${l.user}</div>
                          <div style="font-size: 10px; color: var(--text-dim);">${l.department} (${l.badge_id})</div>
                        </td>
                        <td>
                          <div style="font-size: 11px;">${l.zone_name}</div>
                          <div style="font-size: 9px; color: var(--text-dim);">${l.portal}</div>
                        </td>
                        <td>
                          <span class="badge ${l.status === 'Granted' ? 'badge-healthy' : 'badge-critical'}">
                            ${l.status}
                          </span>
                        </td>
                      </tr>
                    `
                      )
                      .join("")}
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Column 2: CCTV Vision Metadata Events -->
            <div class="glass-panel" style="padding: 16px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h3 style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  CCTV Vision Metadata Events
                </h3>
                <span class="badge badge-purple">AI Computer Vision</span>
              </div>

              <div style="display: flex; flex-direction: column; gap: 10px;">
                ${cctv
                  .map(
                    (c) => `
                  <div style="background: var(--bg-surface-2); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                      <span class="mono" style="font-size: 11px; color: var(--color-primary); font-weight: 700;">${c.timestamp} • ${c.camera_id}</span>
                      <span class="badge ${c.severity === 'Medium' ? 'badge-warning' : c.severity === 'Critical' ? 'badge-critical' : 'badge-good'}" style="font-size: 9px;">
                        ${c.event_type}
                      </span>
                    </div>
                    <div style="font-size: 12px; font-weight: 600; color: #FFF; margin-bottom: 2px;">
                      ${c.location}
                    </div>
                    <p style="font-size: 11px; color: var(--text-muted); line-height: 1.3; margin-bottom: 4px;">
                      ${c.description}
                    </p>
                    <div style="font-size: 10px; color: var(--color-success);">
                      <strong>System Response:</strong> ${c.action_taken} (Confidence: ${Math.round(c.confidence * 100)}%)
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
      el.innerHTML = `<div style="padding: 40px; color: var(--color-danger);">Failed to load security data: ${err.message}</div>`;
    }
  },

  simulateBadgeSwipe() {
    const names = ["Dr. Aris Thorne (Quantum R&D)", "Chief Officer Lisa Sterling", "Tech Specialist Omar Khan", "Guest 44 (Vendor)"];
    const zones = [
      { id: "Z-F2-01", name: "Hardware R&D Lab Alpha", tier: "Restricted", status: "Granted" },
      { id: "Z-F5-01", name: "Mission Critical Data Center", tier: "High-Security", status: "Denied" },
      { id: "Z-F1-01", name: "Main Atrium Reception", tier: "Public", status: "Granted" },
      { id: "Z-F4-01", name: "Executive Boardroom Suite", tier: "Restricted", status: "Granted" }
    ];
    const pickName = names[Math.floor(Math.random() * names.length)];
    const pickZone = zones[Math.floor(Math.random() * zones.length)];

    alert(`[SIMULATED BADGE SWIPE]\nUser: ${pickName}\nPortal: Reader ${pickZone.id}\nResult: ${pickZone.status}\nTier: ${pickZone.tier}`);
    this.render("main-content-view");
  }
};
