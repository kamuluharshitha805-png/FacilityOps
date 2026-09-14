/**
 * FacilityOps API Client & Real-Time WebSocket Manager
 */

const API = {
  baseUrl: (window.location.protocol === "http:" || window.location.protocol === "https:")
    ? (window.location.port ? window.location.origin : `${window.location.protocol}//${window.location.hostname}:8003`)
    : "http://localhost:8003",

    async get(endpoint) {
      try {
        const headers = {};
        if (this.token) headers['Authorization'] = `Bearer ${this.token}`;
        const res = await fetch(`${this.baseUrl}${endpoint}`, { headers });
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        return await res.json();
      } catch (err) {
        console.error(`API GET error on ${endpoint}:`, err);
        throw err;
      }
    },

    async post(endpoint, data = {}) {
      try {
        const headers = { "Content-Type": "application/json" };
        if (this.token) headers['Authorization'] = `Bearer ${this.token}`;
        const res = await fetch(`${this.baseUrl}${endpoint}`, {
          method: "POST",
          headers,
          body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        return await res.json();
      } catch (err) {
        console.error(`API POST error on ${endpoint}:`, err);
        throw err;
      }
    },

    // Login helper
    async login(username, password) {
      const response = await this.post('/api/auth/login', { username, password });
      this.token = response.access_token;
      return response;
    },

    // token storage
    token: null,


  // Telemetry Endpoints
  fetchOverview() {
    return this.get("/api/telemetry/overview");
  },
  fetchZones() {
    return this.get("/api/telemetry/zones");
  },
  fetchZoneDetail(zoneId) {
    return this.get(`/api/telemetry/zones/${zoneId}`);
  },
  fetchAssets() {
    return this.get("/api/telemetry/assets");
  },
  fetchAssetDetail(assetId) {
    return this.get(`/api/telemetry/assets/${assetId}`);
  },

  // Agent Endpoints
  fetchAgentsStatus() {
    return this.get("/api/agents/status");
  },
  fetchInsights() {
    return this.get("/api/agents/insights");
  },
  fetchCorrelations() {
    return this.get("/api/agents/correlations");
  },
  executeRecommendation(insightId) {
    return this.post("/api/agents/execute-recommendation", { insight_id: insightId });
  },
  fetchEnergyDetails() {
    return this.get("/api/agents/energy");
  },
  fetchMaintenanceDetails() {
    return this.get("/api/agents/maintenance");
  },
  fetchOccupancyDetails() {
    return this.get("/api/agents/occupancy");
  },
  fetchSecurityDetails() {
    return this.get("/api/agents/security");
  },
  fetchCostDetails() {
    return this.get("/api/agents/cost");
  },
  fetchExecutiveOverview() {
    return this.get("/api/agents/executive-overview");
  },

  // Alerts Endpoints
  fetchAlerts(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.get(`/api/alerts${query ? "?" + query : ""}`);
  },
  acknowledgeAlert(alertId, user = "Facility Commander") {
    return this.post(`/api/alerts/${alertId}/acknowledge`, { user });
  },
  resolveAlert(alertId) {
    return this.post(`/api/alerts/${alertId}/resolve`, {});
  },

  // Work Orders Endpoints
  fetchWorkOrders(status = null) {
    return this.get(`/api/workorders${status ? "?status=" + status : ""}`);
  },
  createWorkOrder(woData) {
    return this.post("/api/workorders", woData);
  },
  updateWorkOrderStatus(woId, status) {
    return this.post(`/api/workorders/${woId}/status`, { status });
  },

  // Simulation & Scenarios
  fetchScenarios() {
    return this.get("/api/simulation/scenarios");
  },
  injectScenario(scenarioId) {
    return this.post("/api/simulation/inject", { scenario_id: scenarioId });
  },
  stepSimulation() {
    return this.post("/api/simulation/step", {});
  },

  // Reports
  generateReport(period = "Last 24 Hours") {
    return this.get(`/api/reports/generate?period=${encodeURIComponent(period)}`);
  },

  // WebSocket Live Telemetry Streaming
  ws: null,
  wsListeners: new Set(),

  initWebSocket(onMessageCallback) {
    if (onMessageCallback) this.wsListeners.add(onMessageCallback);

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = (window.location.host && window.location.protocol.startsWith("http"))
      ? window.location.host
      : "localhost:8003";
    const wsUrl = `${protocol}//${host}/ws/live`;

    const connect = () => {
      try {
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
          console.log("WebSocket connected to FacilityOps stream.");
          const statusBadge = document.getElementById("ws-status-indicator");
          if (statusBadge) {
            statusBadge.innerHTML = '<span class="beacon-live"></span> LIVE TELEMETRY';
            statusBadge.className = "badge badge-healthy";
          }
        };

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.wsListeners.forEach((listener) => listener(data));
          } catch (e) {
            console.error("WS JSON parse error:", e);
          }
        };

        this.ws.onclose = () => {
          console.warn("WebSocket disconnected. Reconnecting in 3s...");
          const statusBadge = document.getElementById("ws-status-indicator");
          if (statusBadge) {
            statusBadge.innerHTML = '<span class="beacon-critical"></span> DISCONNECTED';
            statusBadge.className = "badge badge-critical";
          }
          setTimeout(connect, 3000);
        };

        this.ws.onerror = (err) => {
          console.error("WebSocket error:", err);
          this.ws.close();
        };
      } catch (err) {
        console.error("Failed to initialize WebSocket:", err);
        setTimeout(connect, 3000);
      }
    };

    connect();
  }
};
