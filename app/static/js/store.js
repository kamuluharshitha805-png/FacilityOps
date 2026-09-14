/**
 * Central Reactive Store for FacilityOps Command Center
 */

const Store = {
  state: {
    persona: "manager", // "manager" | "maintenance" | "security" | "executive"
    activeTab: "command_center",
    selectedFloor: 1,
    heatmapMetric: "occupancy", // "occupancy" | "energy" | "temperature" | "security"
    
    overview: null,
    zones: [],
    assets: [],
    alerts: [],
    workOrders: [],
    insights: [],
    correlations: [],
    scenarios: [],
    activeScenario: "scenario_reset_nominal",
    
    selectedZone: null,
    selectedAsset: null,
    
    alertsFilter: {
      category: "All",
      severity: "All",
      status: "All"
    }
  },

  subscribers: new Set(),

  subscribe(callback) {
    this.subscribers.add(callback);
    return () => this.subscribers.delete(callback);
  },

  notify(event, payload) {
    this.subscribers.forEach((cb) => cb(event, payload, this.state));
  },

  setPersona(persona) {
    this.state.persona = persona;
    // Auto-adjust default view for role convenience if applicable
    if (persona === "maintenance" && this.state.activeTab === "security") {
      this.state.activeTab = "maintenance";
    } else if (persona === "security" && this.state.activeTab === "maintenance") {
      this.state.activeTab = "security";
    } else if (persona === "executive" && !["command_center", "cost", "reports"].includes(this.state.activeTab)) {
      this.state.activeTab = "command_center";
    }
    this.notify("persona_changed", persona);
  },

  setActiveTab(tab) {
    this.state.activeTab = tab;
    this.notify("tab_changed", tab);
  },

  setSelectedFloor(floor) {
    this.state.selectedFloor = parseInt(floor, 10);
    this.notify("floor_changed", this.state.selectedFloor);
  },

  setHeatmapMetric(metric) {
    this.state.heatmapMetric = metric;
    this.notify("heatmap_metric_changed", metric);
  },

  updateOverview(overviewData) {
    this.state.overview = overviewData;
    this.notify("overview_updated", overviewData);
  },

  updateZones(zonesData) {
    this.state.zones = zonesData;
    this.notify("zones_updated", zonesData);
  },

  updateAssets(assetsData) {
    this.state.assets = assetsData;
    this.notify("assets_updated", assetsData);
  },

  updateAlerts(alertsData) {
    this.state.alerts = alertsData;
    this.notify("alerts_updated", alertsData);
  },

  updateWorkOrders(wosData) {
    this.state.workOrders = wosData;
    this.notify("work_orders_updated", wosData);
  },

  updateInsights(insightsData) {
    this.state.insights = insightsData;
    this.notify("insights_updated", insightsData);
  },

  updateCorrelations(corrData) {
    this.state.correlations = corrData;
    this.notify("correlations_updated", corrData);
  }
};
