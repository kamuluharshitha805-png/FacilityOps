/**
 * AI Insight Center Component
 * 5-Pillar Explainable AI: Insight → Why → Risk → Recommendation → Impact
 */

const InsightsComponent = {
  currentFilter: "All",

  async render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-dim);">Loading Explainable AI Insights...</div>`;

    try {
      const insights = await API.fetchInsights();
      Store.updateInsights(insights);

      const filtered =
        this.currentFilter === "All"
          ? insights
          : insights.filter(
              (ins) =>
                ins.agent_source.toLowerCase().includes(this.currentFilter.toLowerCase()) ||
                ins.category.toLowerCase().includes(this.currentFilter.toLowerCase())
            );

      el.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 18px;">
          
          <!-- Header Bar -->
          <div class="glass-panel" style="padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--color-primary);">
                EXPLAINABLE AI RECOMMENDATION SYSTEM • 5-PILLAR CAUSAL REASONING
              </div>
              <h2 style="font-size: 18px; font-weight: 800; color: #FFF; margin: 2px 0;">
                AI Insight Center & Prescriptive Actions
              </h2>
              <p style="font-size: 12px; color: var(--text-muted);">
                Every recommendation provides full root-cause explainability: Insight → Why → Risk → Recommendation → Impact.
              </p>
            </div>
            
            <!-- Agent Source Filter Pills -->
            <div style="display: flex; gap: 4px; background: var(--bg-surface-2); padding: 4px; border-radius: 8px; border: 1px solid var(--border-subtle); flex-wrap: wrap;">
              ${["All", "Energy", "Maintenance", "Occupancy", "Security", "Cost"]
                .map(
                  (cat) => `
                <button 
                  class="btn ${this.currentFilter === cat ? 'btn-primary' : 'btn-outline'}" 
                  style="padding: 4px 10px; font-size: 11px;"
                  onclick="InsightsComponent.setFilter('${cat}')"
                >
                  ${cat}
                </button>
              `
                )
                .join("")}
            </div>
          </div>

          <!-- Insights Stream -->
          <div style="display: flex; flex-direction: column; gap: 14px;">
            ${
              filtered.length === 0
                ? `<div class="glass-panel" style="padding: 40px; text-align: center; color: var(--text-dim);">No active insights found matching filter "${this.currentFilter}".</div>`
                : filtered
                    .map(
                      (ins) => `
                <div class="glass-panel" style="padding: 18px; position: relative;">
                  
                  <!-- Top Row: Priority Badge, Agent Source, Category, Estimated Savings -->
                  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <span class="badge ${ins.priority === 'Critical' ? 'badge-critical' : ins.priority === 'High' ? 'badge-warning' : 'badge-good'}" style="font-size: 11px; padding: 3px 10px;">
                        ${ins.priority} Priority
                      </span>
                      <span style="font-size: 12px; color: var(--color-primary); font-weight: 600;">
                        ${ins.agent_source}
                      </span>
                      <span style="color: var(--text-dim);">•</span>
                      <span style="font-size: 11px; color: var(--text-muted);">
                        ${ins.category}
                      </span>
                    </div>

                    <div style="display: flex; align-items: center; gap: 12px;">
                      ${
                        ins.estimated_savings_usd > 0
                          ? `
                        <span class="badge badge-purple" style="font-size: 11px;">
                          💰 Save ~$${ins.estimated_savings_usd.toLocaleString()}/mo
                        </span>
                      `
                          : ""
                      }
                      <span class="mono" style="font-size: 11px; color: var(--text-dim);">
                        ${ins.timestamp}
                      </span>
                    </div>
                  </div>

                  <!-- Insight Title -->
                  <h3 style="font-size: 16px; font-weight: 800; color: #FFFFFF; margin-bottom: 12px;">
                    ${ins.title}
                  </h3>

                  <!-- 5-Pillar Explainable AI Grid -->
                  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; background: var(--bg-surface-1); padding: 14px; border-radius: 8px; border: 1px solid var(--border-subtle); margin-bottom: 14px;">
                    
                    <!-- 1. INSIGHT -->
                    <div>
                      <div class="insight-pillar-title" style="color: #38BDF8;">
                        ① INSIGHT (What happened?)
                      </div>
                      <p class="insight-pillar-desc">
                        ${ins.insight}
                      </p>
                    </div>

                    <!-- 2. WHY -->
                    <div>
                      <div class="insight-pillar-title" style="color: #A855F7;">
                        ② WHY (Why did it happen?)
                      </div>
                      <p class="insight-pillar-desc">
                        ${ins.why}
                      </p>
                    </div>

                    <!-- 3. RISK -->
                    <div>
                      <div class="insight-pillar-title" style="color: #EF4444;">
                        ③ RISK (What if no action?)
                      </div>
                      <p class="insight-pillar-desc" style="color: #FCA5A5;">
                        ${ins.risk}
                      </p>
                    </div>

                    <!-- 4. RECOMMENDATION -->
                    <div>
                      <div class="insight-pillar-title" style="color: #10B981;">
                        ④ RECOMMENDATION (What to do?)
                      </div>
                      <p class="insight-pillar-desc">
                        ${ins.recommendation}
                      </p>
                    </div>

                    <!-- 5. IMPACT -->
                    <div>
                      <div class="insight-pillar-title" style="color: #F59E0B;">
                        ⑤ IMPACT (Expected Benefit)
                      </div>
                      <p class="insight-pillar-desc" style="color: #FDE68A;">
                        ${ins.impact}
                      </p>
                    </div>

                  </div>

                  <!-- Action Footer -->
                  <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 12px;">
                    <div style="font-size: 11px; color: var(--text-dim);">
                      ${
                        ins.is_executed
                          ? `<span style="color: var(--color-success); font-weight: 700;">✓ Optimization Executed on ${ins.executed_at}</span>`
                          : `Autonomous AI prescription ready for execution.`
                      }
                    </div>

                    ${
                      !ins.is_executed
                        ? `
                      <button class="btn btn-primary" onclick="InsightsComponent.executeInsight('${ins.id}')">
                        ⚡ ${ins.action_label}
                      </button>
                    `
                        : `
                      <button class="btn btn-outline" disabled style="opacity: 0.6; cursor: default;">
                        ✓ Completed
                      </button>
                    `
                    }
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
      el.innerHTML = `<div style="padding: 40px; color: var(--color-danger);">Failed to load insights: ${err.message}</div>`;
    }
  },

  setFilter(filter) {
    this.currentFilter = filter;
    this.render("main-content-view");
  },

  async executeInsight(insightId) {
    try {
      await API.executeRecommendation(insightId);
      alert("Autonomous optimization executed. Telemetry updated across all agents.");
      this.render("main-content-view");
    } catch (err) {
      alert("Execution error: " + err.message);
    }
  }
};
