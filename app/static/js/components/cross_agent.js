/**
 * Cross-Agent Intelligence Orchestration Component
 * The Core Differentiator: Unifies Energy, Maintenance, Occupancy, Security & Cost
 */

const CrossAgentComponent = {
  async render(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-dim);">Loading Cross-Agent Orchestration Telemetry...</div>`;

    try {
      const correlations = await API.fetchCorrelations();
      Store.updateCorrelations(correlations);
      const agents = await API.fetchAgentsStatus();

      el.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 18px;">
          
          <!-- Header Bar -->
          <div class="glass-panel" style="padding: 16px 20px; background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--color-purple);">
                CENTRAL NERVOUS SYSTEM • CROSS-AGENT ORCHESTRATION ENGINE
              </div>
              <h2 style="font-size: 18px; font-weight: 800; color: #FFF; margin: 2px 0;">
                Multi-Agent Synthesis & Cross-Correlation Matrix
              </h2>
              <p style="font-size: 12px; color: var(--text-muted);">
                Autonomous agents do not operate in silos. Every event is cross-correlated to reveal hidden facility root causes.
              </p>
            </div>
            <div style="display: flex; gap: 10px;">
              <span class="badge badge-purple" style="font-size: 11px;">
                ⚡ 5 Active Neural Bridges
              </span>
            </div>
          </div>

          <!-- Multi-Agent Node Architecture Map -->
          <div class="glass-panel" style="padding: 20px;">
            <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF; margin-bottom: 6px;">
              Autonomous Multi-Agent Topology
            </h3>
            <p style="font-size: 11px; color: var(--text-muted); margin-bottom: 16px;">
              Real-time synchronization status, inference latencies, and processed telemetry counts across all 5 specialized agents.
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
              ${agents
                .map(
                  (a) => `
                <div style="background: var(--bg-surface-2); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between;">
                  <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                      <span class="badge badge-good" style="font-size: 9px;">${a.status}</span>
                      <span class="mono" style="font-size: 10px; color: var(--text-dim);">${a.latency_ms} ms</span>
                    </div>
                    <div style="font-size: 13px; font-weight: 700; color: #FFF; margin-bottom: 2px;">${a.name}</div>
                    <div style="font-size: 10px; color: var(--text-dim); margin-bottom: 8px;">${a.role}</div>
                  </div>
                  <div style="border-top: 1px solid var(--border-subtle); padding-top: 8px; font-size: 10px; color: var(--text-muted); display: flex; justify-content: space-between;">
                    <span>Points: ${a.telemetry_points_processed.toLocaleString()}</span>
                    <span>Alerts: ${a.alerts_generated}</span>
                  </div>
                </div>
              `
                )
                .join("")}
            </div>
          </div>

          <!-- Active Cross-Agent Correlation Streams -->
          <div class="glass-panel" style="padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
              <div>
                <h3 style="font-size: 14px; font-weight: 700; text-transform: uppercase; color: #FFF;">
                  Active Cross-Correlation Reasoning Pipelines (${correlations.length})
                </h3>
                <p style="font-size: 11px; color: var(--text-muted);">
                  The AI continuously validates multi-variate telemetry across disparate building systems to identify compounding risks.
                </p>
              </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 14px;">
              ${correlations
                .map(
                  (c) => `
                <div style="background: var(--bg-surface-2); border: 1px solid var(--border-medium); border-radius: 10px; padding: 16px; position: relative;">
                  <!-- Header: Pair badge, Rule name, Match Confidence -->
                  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <span class="badge badge-purple" style="font-size: 11px; padding: 3px 10px;">
                        🔗 ${c.pair}
                      </span>
                      <h4 style="font-size: 14px; font-weight: 700; color: #FFFFFF;">
                        ${c.correlation_rule}
                      </h4>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <span class="badge badge-healthy" style="font-size: 10px;">
                        Confidence: ${c.confidence_pct}%
                      </span>
                      <span class="mono" style="font-size: 10px; color: var(--text-dim);">${c.timestamp}</span>
                    </div>
                  </div>

                  <!-- 2-Node Event Causality Chain -->
                  <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 10px; align-items: center; background: var(--bg-surface-1); padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid var(--border-subtle);">
                    <!-- Event A -->
                    <div style="border-left: 3px solid #38BDF8; padding-left: 10px;">
                      <div style="font-size: 10px; text-transform: uppercase; color: #38BDF8; font-weight: 700;">
                        Primary Event • ${c.agent_a}
                      </div>
                      <div style="font-size: 12px; color: #F1F5F9; margin-top: 2px;">
                        ${c.event_a}
                      </div>
                    </div>

                    <!-- Synthesis Connector -->
                    <div style="display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; background: rgba(168, 85, 247, 0.2); border-radius: 50%; color: #C084FC; font-size: 14px; font-weight: 800;">
                      ⟷
                    </div>

                    <!-- Event B -->
                    <div style="border-left: 3px solid #F59E0B; padding-left: 10px;">
                      <div style="font-size: 10px; text-transform: uppercase; color: #F59E0B; font-weight: 700;">
                        Correlated Event • ${c.agent_b}
                      </div>
                      <div style="font-size: 12px; color: #F1F5F9; margin-top: 2px;">
                        ${c.event_b}
                      </div>
                    </div>
                  </div>

                  <!-- AI Synthesis Reasoning -->
                  <div style="margin-bottom: 10px;">
                    <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--color-purple); margin-bottom: 2px;">
                      🧠 Multi-Agent AI Synthesis Reasoning
                    </div>
                    <p style="font-size: 12px; color: var(--text-muted); line-height: 1.5;">
                      ${c.ai_reasoning}
                    </p>
                  </div>

                  <!-- Unified Action & Impact Footer -->
                  <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 10px 14px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                      <div style="font-size: 10px; text-transform: uppercase; color: var(--color-success); font-weight: 700;">
                        Prescribed Unified Intervention
                      </div>
                      <div style="font-size: 12px; font-weight: 600; color: #FFFFFF;">
                        ${c.recommended_unified_action}
                      </div>
                    </div>
                    <div style="text-align: right;">
                      <div style="font-size: 10px; text-transform: uppercase; color: var(--text-dim);">
                        Risk / Financial Avoidance
                      </div>
                      <div style="font-size: 12px; font-weight: 700; color: #6EE7B7;">
                        ${c.financial_or_risk_impact}
                      </div>
                    </div>
                  </div>

                </div>
              `
                )
                .join("")}
            </div>
          </div>

        </div>
      `;
    } catch (err) {
      el.innerHTML = `<div style="padding: 40px; color: var(--color-danger);">Failed to load cross-agent data: ${err.message}</div>`;
    }
  }
};
