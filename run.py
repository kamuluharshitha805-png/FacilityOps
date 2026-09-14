"""
FacilityOps AI Platform — One-Click Runner
Starts the FastAPI server with real-time IoT simulation and Single Page Command Center.
"""

import sys
import uvicorn

def main():
    print("=" * 75)
    print("  FACILITYOPS AI PLATFORM // AUTONOMOUS FACILITY OPERATING SYSTEM")
    print("=" * 75)
    print("  Building:      Apex Tower Global HQ (5 Floors, 24 Zones, 50+ Assets)")
    print("  AI Agents:     Energy, Maintenance, Occupancy, Security, Cost, Orchestrator")
    print("  Intelligence:  Explainable AI (Insight -> Why -> Risk -> Rec -> Impact)")
    print("  URL:           http://127.0.0.1:8000")
    print("  API Docs:      http://127.0.0.1:8000/docs")
    print("  Live Stream:   ws://127.0.0.1:8000/ws/live")
    print("=" * 75)
    print("Starting server... Press Ctrl+C to terminate.\n")

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
