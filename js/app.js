/**
 * Main Application Controller for FacilityOps Command Center
 */

const App = {
  async init() {
    console.log("Initializing FacilityOps AI Operating System UI...");

    // 1. Render Global Header & Scenario Bar
    HeaderComponent.render("header-container");

    // 2. Fetch Initial Enterprise Telemetry
    try {
      const results = await Promise.allSettled([
        API.fetchOverview(),
        API.fetchZones(),
        API.fetchAssets(),
        API.fetchAlerts(),
        API.fetchWorkOrders(),
        API.fetchInsights(),
        API.fetchCorrelations()
      ]);

      const [overview, zones, assets, alerts, workOrders, insights, correlations] = results.map(
        (r) => (r.status === "fulfilled" ? r.value : null)
      );

      if (overview) {
        Store.updateOverview(overview);
        if (overview.facility_health_score !== undefined) {
          HeaderComponent.updateHealthScore(overview.facility_health_score);
        }
      }
      if (zones) Store.updateZones(zones);
      if (assets) Store.updateAssets(assets);
      if (alerts) Store.updateAlerts(alerts);
      if (workOrders) Store.updateWorkOrders(workOrders);
      if (insights) Store.updateInsights(insights);
      if (correlations) Store.updateCorrelations(correlations);
    } catch (err) {
      console.error("Initial data load failed:", err);
    }

    // 3. Connect Real-Time WebSocket Telemetry Streaming
    API.initWebSocket((data) => {
      if (data.type === "telemetry_tick" || data.type === "initial_state" || data.type === "telemetry_update") {
        const ov = data.overview || data.data;
        if (ov) {
          Store.updateOverview(ov);
          if (ov.facility_health_score !== undefined) {
            HeaderComponent.updateHealthScore(ov.facility_health_score);
          }
        }

        // If on Executive Command Center, update real-time view
        if (Store.state.activeTab === "command_center") {
          ExecutiveComponent.render("main-content-view");
        }
      }
    });

    // 4. Subscribe to Store State Changes
    Store.subscribe((event, payload, state) => {
      if (event === "tab_changed" || event === "persona_changed" || event === "overview_updated") {
        this.renderActiveTab();
      }
    });

    // 5. Initial View Render
    this.renderActiveTab();
  },

  switchTab(tabId) {
    Store.setActiveTab(tabId);
    
    // Update Tab UI active styles
    document.querySelectorAll(".nav-tab").forEach((tab) => {
      const isActive = tab.dataset.tab === tabId;
      tab.classList.toggle("active", isActive);
    });
  },

  renderActiveTab() {
    const tab = Store.state.activeTab;
    const viewContainer = "main-content-view";

    // Synchronize tab button styles
    document.querySelectorAll(".nav-tab").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.tab === tab);
    });

    switch (tab) {
      case "command_center":
        ExecutiveComponent.render(viewContainer);
        break;
      case "energy":
        EnergyComponent.render(viewContainer);
        break;
      case "maintenance":
        MaintenanceComponent.render(viewContainer);
        break;
      case "occupancy":
        OccupancyComponent.render(viewContainer);
        break;
      case "security":
        SecurityComponent.render(viewContainer);
        break;
      case "cross_agent":
        CrossAgentComponent.render(viewContainer);
        break;
      case "cost":
        CostComponent.render(viewContainer);
        break;
      case "insights":
        InsightsComponent.render(viewContainer);
        break;
      case "alerts":
        AlertsComponent.render(viewContainer);
        break;
      case "reports":
        ReportsComponent.render(viewContainer);
        break;
      default:
        ExecutiveComponent.render(viewContainer);
    }
  }
};

// Bootstrap application once DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  App.init();
});
