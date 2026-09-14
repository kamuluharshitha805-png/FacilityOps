/**
 * Occupancy Intelligence Component
 * Space Utilization, Multi-Floor Interactive Heatmaps & Visitor Flow
 */

const OccupancyComponent = {
  async render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-dim);">Loading Occupancy Telemetry...</div>`;

    try {
      const data = await API.fetchOccupancyDetails();
      const zones = await API.fetchZones();
      Store.updateZones(zones);
      const kpis = data.kpis;
      const dist = kpis.zone_distribution || { crowded: 2, normal: 15, low: 5, empty: 2 };
      const floors = kpis.floor_breakdown || [];

      el.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 18px;">
          
          <!-- Header Bar -->
          <div class="glass-panel" style="padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--color-primary);">
                Autonomous Occupancy Intelligence Agent (agt_occupancy_03)
              </div>
              <h2 style="font-size: 18px; font-weight: 800; color: #FFF; margin: 2px 0;">
                Spatial Density, Heatmaps & Space Utilization
              </h2>
              <p style="font-size: 12px; color: var(--text-muted);">
                Translates physical presence telemetry into thermal comfort, lighting automation, and real-estate efficiency.
              </p>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
              <span class="badge ${kpis.space_utilization_score >= 80 ? 'badge-healthy' : 'badge-warning'}">
                Space Score: ${kpis.space_utilization_score}%
              </span>
            </div>
          </div>

          <!-- Occupancy KPIs -->
          <div class="kpi-grid">
            <div class="kpi-card" style="--card-accent: #818CF8;">
              <div class="kpi-title">Current Occupancy</div>
              <div class="kpi-value">${kpis.current_occupancy} <span style="font-size: 14px; color: var(--text-dim);">/ ${kpis.total_capacity}</span></div>
              <div class="kpi-footer">
                <span>Occupancy Rate:</span>
                <span style="color: var(--color-accent); font-weight: 700;">${kpis.occupancy_rate}%</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #38BDF8;">
              <div class="kpi-title">Peak Headcount</div>
              <div class="kpi-value">${kpis.peak_occupancy}</div>
              <div class="kpi-footer">
                <span>Building Peak</span>
                <span style="color: var(--color-primary);">Diurnal High</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #10B981;">
              <div class="kpi-title">Authorized Visitors</div>
              <div class="kpi-value">${kpis.visitor_count}</div>
              <div class="kpi-footer">
                <span>Active Badges</span>
                <span style="color: var(--color-success);">Floor 1 & 3 Hubs</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #F59E0B;">
              <div class="kpi-title">Active Zones</div>
              <div class="kpi-value">${kpis.active_zones_count} <span style="font-size: 14px; color: var(--text-dim);">/ 24</span></div>
              <div class="kpi-footer">
                <span>Underutilized: ${kpis.underutilized_zones_count}</span>
                <span style="color: var(--color-warning);">Crowded: ${kpis.crowded_zones_count}</span>
              </div>
            </div>

            <div class="kpi-card" style="--card-accent: #A855F7;">
              <div class="kpi-title">Space Utilization Index</div>
              <div class="kpi-value" style="color: #E9D5FF;">${kpis.space_utilization_score}%</div>
              <div class="kpi-footer">
                <span>Target: 70-85%</span>
                <span style="color: var(--color-purple); font-weight: 700;">Optimal Range</span>
              </div>
            </div>
          </div>

          <!-- Primary Visualization: Zone Occupancy Distribution -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Primary Visualization: Zone Occupancy Distribution
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  Categorized zone capacity utilization: Crowded (>80%), Normal (35-80%), Low (5-35%), Empty (<5%).
                </p>
              </div>
              <span class="mono" style="font-size: 12px; color: var(--color-primary); font-weight: 700;">
                24 Monitored Zones
              </span>
            </div>

            <div style="height: 32px; width: 100%; border-radius: 6px; overflow: hidden; display: flex; margin-bottom: 14px; border: 1px solid var(--border-medium);">
              <div style="width: ${(dist.crowded / 24) * 100}%; background: #EF4444; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #FFF;">
                ${dist.crowded} Crowded
              </div>
              <div style="width: ${(dist.normal / 24) * 100}%; background: #10B981; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #FFF;">
                ${dist.normal} Normal
              </div>
              <div style="width: ${(dist.low / 24) * 100}%; background: #38BDF8; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #FFF;">
                ${dist.low} Low
              </div>
              <div style="width: ${(dist.empty / 24) * 100}%; background: #475569; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #FFF;">
                ${dist.empty} Empty
              </div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
              <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px; border-left: 3px solid #EF4444;">
                <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Crowded (>80%)</div>
                <div style="font-size: 18px; font-weight: 700; color: #EF4444;">${dist.crowded} Zones</div>
              </div>
              <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px; border-left: 3px solid #10B981;">
                <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Normal (35-80%)</div>
                <div style="font-size: 18px; font-weight: 700; color: #10B981;">${dist.normal} Zones</div>
              </div>
              <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px; border-left: 3px solid #38BDF8;">
                <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Low Occupancy (5-35%)</div>
                <div style="font-size: 18px; font-weight: 700; color: #38BDF8;">${dist.low} Zones</div>
              </div>
              <div style="background: var(--bg-surface-2); padding: 10px; border-radius: 6px; border-left: 3px solid #64748B;">
                <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Empty (<5%)</div>
                <div style="font-size: 18px; font-weight: 700; color: #94A3B8;">${dist.empty} Zones</div>
              </div>
            </div>
          </div>

          <!-- Interactive Multi-Floor SVG Heatmap Viewer -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Interactive Floorplan & Real-Time Heatmap
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  Drill down into floor zones, monitor environmental sensors, and inspect installed assets.
                </p>
              </div>

              <!-- Floor & Metric Selectors -->
              <div style="display: flex; align-items: center; gap: 10px;">
                <!-- Floor Selector -->
                <div style="display: flex; gap: 4px; background: var(--bg-surface-2); padding: 3px; border-radius: 6px; border: 1px solid var(--border-subtle);">
                  ${[1, 2, 3, 4, 5]
                    .map(
                      (fl) => `
                    <button 
                      class="btn ${Store.state.selectedFloor === fl ? 'btn-primary' : 'btn-outline'}" 
                      style="padding: 4px 10px; font-size: 11px;"
                      onclick="OccupancyComponent.changeFloor(${fl})"
                    >
                      L0${fl}
                    </button>
                  `
                    )
                    .join("")}
                </div>

                <!-- Layer Selector -->
                <select 
                  id="heatmap-layer-select" 
                  onchange="OccupancyComponent.changeLayer(this.value)"
                  style="background: var(--bg-surface-2); color: #FFF; border: 1px solid var(--border-medium); padding: 6px 10px; border-radius: 6px; font-size: 11px;"
                >
                  <option value="occupancy" ${Store.state.heatmapMetric === 'occupancy' ? 'selected' : ''}>Layer: Occupancy Density</option>
                  <option value="energy" ${Store.state.heatmapMetric === 'energy' ? 'selected' : ''}>Layer: Power & Energy</option>
                  <option value="temperature" ${Store.state.heatmapMetric === 'temperature' ? 'selected' : ''}>Layer: Temperature & Climate</option>
                  <option value="security" ${Store.state.heatmapMetric === 'security' ? 'selected' : ''}>Layer: Security Tiers & Alarms</option>
                </select>
              </div>
            </div>

            <!-- SVG Container -->
            <div id="occupancy-floorplan-container"></div>
          </div>

          <!-- Floor-by-Floor Breakdown Table -->
          <div class="glass-panel" style="padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                Building Floor Utilization Drill-Down
              </h3>
            </div>

            <div class="table-container">
              <table class="facility-table">
                <thead>
                  <tr>
                    <th>Floor Level</th>
                    <th>Headcount</th>
                    <th>Capacity</th>
                    <th>Occupancy Rate</th>
                    <th>Active Zones</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  ${floors
                    .map(
                      (fl) => `
                    <tr>
                      <td class="mono" style="font-weight: 700; color: var(--color-primary);">Level 0${fl.floor}</td>
                      <td class="mono" style="font-weight: 700;">${fl.occupancy}</td>
                      <td class="mono">${fl.capacity}</td>
                      <td>
                        <div style="display: flex; align-items: center; gap: 8px;">
                          <div style="width: 80px; height: 6px; background: var(--bg-surface-3); border-radius: 3px; overflow: hidden;">
                            <div style="width: ${fl.rate_pct}%; height: 100%; background: ${fl.rate_pct > 75 ? 'var(--color-warning)' : 'var(--color-primary)'};"></div>
                          </div>
                          <span class="mono">${fl.rate_pct}%</span>
                        </div>
                      </td>
                      <td class="mono">${fl.active_zones} / ${fl.total_zones}</td>
                      <td>
                        <span class="badge ${fl.rate_pct > 75 ? 'badge-warning' : fl.rate_pct > 20 ? 'badge-healthy' : 'badge-good'}">
                          ${fl.rate_pct > 75 ? 'High Density' : fl.rate_pct > 20 ? 'Nominal' : 'Low Activity'}
                        </span>
                      </td>
                      <td>
                        <button class="btn btn-outline" style="padding: 2px 8px; font-size: 10px;" onclick="OccupancyComponent.changeFloor(${fl.floor})">
                          Inspect L0${fl.floor} →
                        </button>
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

      // Render the SVG Floorplan
      FloorPlan.render(
        "occupancy-floorplan-container",
        Store.state.selectedFloor,
        zones,
        Store.state.heatmapMetric
      );
    } catch (err) {
      el.innerHTML = `<div style="padding: 40px; color: var(--color-danger);">Failed to load occupancy data: ${err.message}</div>`;
    }
  },

  changeFloor(floorNum) {
    Store.setSelectedFloor(floorNum);
    this.render("main-content-view");
  },

  changeLayer(metric) {
    Store.setHeatmapMetric(metric);
    FloorPlan.render(
      "occupancy-floorplan-container",
      Store.state.selectedFloor,
      Store.state.zones,
      metric
    );
  }
};
