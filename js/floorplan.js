/**
 * Interactive Architectural SVG Floor Plan & Multi-Layer Heatmap Renderer
 */

const FloorPlan = {
  // Zone layout coordinates for a 800x420 architectural viewBox
  // 5 distinct structural zones per floor
  zoneLayouts: [
    { x: 30,  y: 30,  w: 360, h: 170, labelPos: { x: 210, y: 110 } }, // Zone 1 (NW Wing)
    { x: 410, y: 30,  w: 360, h: 170, labelPos: { x: 590, y: 110 } }, // Zone 2 (NE Wing)
    { x: 30,  y: 220, w: 230, h: 170, labelPos: { x: 145, y: 300 } }, // Zone 3 (SW Core)
    { x: 280, y: 220, w: 240, h: 170, labelPos: { x: 400, y: 300 } }, // Zone 4 (Central Core)
    { x: 540, y: 220, w: 230, h: 170, labelPos: { x: 655, y: 300 } }, // Zone 5 (SE Utility Wing)
  ],

  getColor(zone, metric) {
    if (zone.is_anomaly) {
      return { fill: "rgba(239, 68, 68, 0.45)", stroke: "#EF4444", text: "#FCA5A5" };
    }

    if (metric === "occupancy") {
      const rate = zone.occupancy_rate || 0;
      if (rate >= 80) return { fill: "rgba(239, 68, 68, 0.3)", stroke: "#EF4444", text: "#FCA5A5" };
      if (rate >= 40) return { fill: "rgba(16, 185, 129, 0.25)", stroke: "#10B981", text: "#6EE7B7" };
      if (rate > 5)   return { fill: "rgba(56, 189, 248, 0.2)", stroke: "#38BDF8", text: "#BAE6FD" };
      return { fill: "rgba(51, 65, 85, 0.2)", stroke: "#475569", text: "#94A3B8" };
    }

    if (metric === "energy") {
      const kw = zone.power_draw_kw || 10;
      if (kw > 40) return { fill: "rgba(239, 68, 68, 0.35)", stroke: "#EF4444", text: "#FCA5A5" };
      if (kw > 25) return { fill: "rgba(245, 158, 11, 0.3)", stroke: "#F59E0B", text: "#FDE68A" };
      return { fill: "rgba(56, 189, 248, 0.22)", stroke: "#38BDF8", text: "#BAE6FD" };
    }

    if (metric === "temperature") {
      const temp = zone.temperature_c || 22.0;
      if (temp > 23.5) return { fill: "rgba(239, 68, 68, 0.3)", stroke: "#EF4444", text: "#FCA5A5" };
      if (temp < 20.0) return { fill: "rgba(99, 102, 241, 0.3)", stroke: "#6366F1", text: "#C7D2FE" };
      return { fill: "rgba(16, 185, 129, 0.22)", stroke: "#10B981", text: "#6EE7B7" };
    }

    if (metric === "security") {
      const sec = zone.security || "Public";
      if (sec === "High-Security") return { fill: "rgba(239, 68, 68, 0.28)", stroke: "#EF4444", text: "#FCA5A5" };
      if (sec === "Restricted")    return { fill: "rgba(245, 158, 11, 0.25)", stroke: "#F59E0B", text: "#FDE68A" };
      if (sec === "Operational")   return { fill: "rgba(168, 85, 247, 0.2)", stroke: "#A855F7", text: "#E9D5FF" };
      return { fill: "rgba(56, 189, 248, 0.15)", stroke: "#38BDF8", text: "#BAE6FD" };
    }

    return { fill: "rgba(56, 189, 248, 0.2)", stroke: "#38BDF8", text: "#BAE6FD" };
  },

  render(containerId, floorNum, zones, metric = "occupancy") {
    const container = document.getElementById(containerId);
    if (!container) return;

    const floorZones = zones.filter((z) => z.floor === floorNum);

    let zonesSvg = "";
    floorZones.forEach((z, index) => {
      const layout = this.zoneLayouts[index % this.zoneLayouts.length];
      const colors = this.getColor(z, metric);

      // Primary Metric Text Display
      let metricLine = "";
      if (metric === "occupancy") {
        metricLine = `Occ: ${z.current_occupancy}/${z.capacity} (${z.occupancy_rate}%)`;
      } else if (metric === "energy") {
        metricLine = `Power: ${z.power_draw_kw} kW`;
      } else if (metric === "temperature") {
        metricLine = `Temp: ${z.temperature_c}°C / Set: ${z.target_temperature_c}°C`;
      } else if (metric === "security") {
        metricLine = `Tier: ${z.security} | ${z.motion_detected ? "Motion Active" : "Clear"}`;
      }

      const isAnomaly = z.is_anomaly;

      zonesSvg += `
        <g class="zone-group" onclick="FloorPlan.inspectZone('${z.id}')" style="cursor: pointer;">
          <!-- Zone Boundary Box -->
          <rect 
            class="zone-rect" 
            x="${layout.x}" 
            y="${layout.y}" 
            width="${layout.w}" 
            height="${layout.h}" 
            rx="8" 
            fill="${colors.fill}" 
            stroke="${colors.stroke}" 
            stroke-width="1.8" 
          />
          
          <!-- Zone Header Bar -->
          <rect x="${layout.x}" y="${layout.y}" width="${layout.w}" height="30" rx="8" fill="rgba(15, 23, 42, 0.65)" />
          
          <!-- Zone Identifier & Security Pill -->
          <text x="${layout.x + 12}" y="${layout.y + 20}" fill="#F8FAFC" font-size="12" font-weight="700" font-family="monospace">
            ${z.id}
          </text>
          
          <text x="${layout.x + layout.w - 12}" y="${layout.y + 20}" text-anchor="end" fill="${colors.text}" font-size="10" font-weight="600">
            ${z.security}
          </text>

          <!-- Zone Display Name -->
          <text x="${layout.labelPos.x}" y="${layout.labelPos.y - 12}" text-anchor="middle" fill="#FFFFFF" font-size="13" font-weight="600">
            ${z.name}
          </text>

          <!-- Real-Time Metric Display -->
          <text x="${layout.labelPos.x}" y="${layout.labelPos.y + 14}" text-anchor="middle" fill="${colors.text}" font-size="12" font-weight="700" font-family="monospace">
            ${metricLine}
          </text>

          <!-- Area & Sub-reading -->
          <text x="${layout.labelPos.x}" y="${layout.labelPos.y + 36}" text-anchor="middle" fill="#94A3B8" font-size="10">
            ${z.area_sqft.toLocaleString()} sqft | CO₂: ${z.co2_ppm} ppm | RH: ${z.humidity_pct}%
          </text>

          ${
            isAnomaly
              ? `
            <circle cx="${layout.x + layout.w - 20}" cy="${layout.y + layout.h - 20}" r="8" fill="#EF4444" class="beacon-critical" />
            <text x="${layout.x + layout.w - 34}" y="${layout.y + layout.h - 16}" text-anchor="end" fill="#FCA5A5" font-size="10" font-weight="700">
              ANOMALY
            </text>
          `
              : ""
          }
        </g>
      `;
    });

    const svgHtml = `
      <div style="position: relative; width: 100%;">
        <svg viewBox="0 0 800 420" class="floorplan-svg" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255, 255, 255, 0.03)" stroke-width="1" />
            </pattern>
          </defs>

          <!-- Blueprint Background Grid -->
          <rect width="800" height="420" fill="#0B1120" rx="14" />
          <rect width="800" height="420" fill="url(#grid)" rx="14" />

          <!-- Exterior Perimeter Wall -->
          <rect x="15" y="15" width="770" height="390" rx="12" fill="none" stroke="#334155" stroke-width="3" stroke-dasharray="8 4" />

          <!-- Floor Level Label & Legend -->
          <text x="25" y="405" fill="#64748B" font-size="11" font-weight="600" font-family="monospace">
            APEX TOWER • LEVEL 0${floorNum} ARCHITECTURAL SCHEMATIC • LAYER: ${metric.toUpperCase()}
          </text>
          <text x="775" y="405" text-anchor="end" fill="#64748B" font-size="10">
            Click any zone to inspect live environmental telemetry & equipment
          </text>

          <!-- Zones -->
          ${zonesSvg}
        </svg>
      </div>
    `;

    container.innerHTML = svgHtml;
  },

  async inspectZone(zoneId) {
    try {
      const data = await API.fetchZoneDetail(zoneId);
      const zone = data.zone;
      const assets = data.assets || [];

      const modalHtml = `
        <div class="modal-backdrop" id="zone-modal">
          <div class="modal-content">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
              <div>
                <div class="badge ${zone.is_anomaly ? 'badge-critical' : 'badge-good'}" style="margin-bottom: 6px;">
                  Level 0${zone.floor} • ${zone.id}
                </div>
                <h3 style="font-size: 18px; color: #FFF;">${zone.name}</h3>
                <p style="color: var(--text-muted); font-size: 12px;">Type: ${zone.type} | Security Tier: <strong>${zone.security}</strong> | Area: ${zone.area_sqft.toLocaleString()} sq.ft.</p>
              </div>
              <button class="btn btn-outline" onclick="document.getElementById('zone-modal').remove()">✕ Close</button>
            </div>

            <!-- Environmental Telemetry Grid -->
            <div class="kpi-grid" style="grid-template-columns: repeat(3, 1fr); margin-bottom: 16px;">
              <div class="kpi-card">
                <div class="kpi-title">Occupancy</div>
                <div class="kpi-value">${zone.current_occupancy} <span style="font-size: 14px; color: var(--text-dim);">/ ${zone.capacity}</span></div>
                <div class="kpi-footer">Rate: ${zone.occupancy_rate}%</div>
              </div>
              <div class="kpi-card">
                <div class="kpi-title">Temperature</div>
                <div class="kpi-value">${zone.temperature_c}°C</div>
                <div class="kpi-footer">Setpoint: ${zone.target_temperature_c}°C</div>
              </div>
              <div class="kpi-card">
                <div class="kpi-title">Air Quality & Power</div>
                <div class="kpi-value">${zone.power_draw_kw} <span style="font-size: 12px;">kW</span></div>
                <div class="kpi-footer">CO₂: ${zone.co2_ppm} ppm | RH: ${zone.humidity_pct}%</div>
              </div>
            </div>

            <!-- Installed Assets in this Zone -->
            <h4 style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: var(--color-primary); margin-bottom: 8px;">
              Installed Assets & Equipment (${assets.length})
            </h4>
            
            ${
              assets.length === 0
                ? `<p style="color: var(--text-dim); font-size: 12px;">No primary industrial equipment directly mapped to this zone floor.</p>`
                : `
              <table class="facility-table">
                <thead>
                  <tr>
                    <th>Tag</th>
                    <th>Asset Name</th>
                    <th>Type</th>
                    <th>Health Score</th>
                    <th>Power</th>
                    <th>Vibration</th>
                  </tr>
                </thead>
                <tbody>
                  ${assets
                    .map(
                      (a) => `
                    <tr>
                      <td class="mono" style="font-weight: 700; color: var(--color-primary);">${a.id}</td>
                      <td>${a.name}</td>
                      <td>${a.type}</td>
                      <td>
                        <span class="badge ${a.health_score >= 85 ? 'badge-healthy' : a.health_score >= 70 ? 'badge-good' : a.health_score >= 50 ? 'badge-warning' : 'badge-critical'}">
                          ${a.health_score}%
                        </span>
                      </td>
                      <td class="mono">${a.current_kw} kW</td>
                      <td class="mono">${a.vibration_rms} mm/s</td>
                    </tr>
                  `
                    )
                    .join("")}
                </tbody>
              </table>
            `
            }

            <div style="margin-top: 20px; display: flex; justify-content: flex-end; gap: 10px;">
              <button class="btn btn-outline" onclick="FloorPlan.adjustZoneSetpoint('${zone.id}')">Adjust HVAC Setpoint</button>
              <button class="btn btn-primary" onclick="document.getElementById('zone-modal').remove()">Done</button>
            </div>
          </div>
        </div>
      `;

      const existing = document.getElementById("zone-modal");
      if (existing) existing.remove();
      document.body.insertAdjacentHTML("beforeend", modalHtml);
    } catch (err) {
      console.error("Failed to inspect zone:", err);
    }
  },

  async adjustZoneSetpoint(zoneId) {
    const newTemp = prompt("Enter new target temperature setpoint (°C) [19.0 - 24.5]:", "21.5");
    if (!newTemp || isNaN(parseFloat(newTemp))) return;

    const val = parseFloat(newTemp);
    const zone = Store.state.zones.find((z) => z.id === zoneId);
    if (zone) {
      zone.target_temperature_c = val;
      alert(`HVAC setpoint updated for ${zone.name} to ${val}°C.`);
      const modal = document.getElementById("zone-modal");
      if (modal) modal.remove();
      this.inspectZone(zoneId);
    }
  }
};
