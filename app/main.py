"""
FastAPI application entrypoint for the Agentic FacilityOps AI Platform.
Provides REST APIs, WebSocket live telemetry streaming, and serves the Single Page Command Center UI.
"""

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import (
    routes_telemetry,
    routes_agents,
    routes_alerts,
    routes_workorders,
    routes_simulation,
    routes_reports,
    routes_auth,
)
from app.engine.simulator import simulator_instance

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("facilityops")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Active WebSocket clients
connected_clients: Set[WebSocket] = set()

async def simulation_background_loop():
    logger.info("Simulation background loop started.")
    while True:
        try:
            simulator_instance.step_simulation()
            
            # Broadcast telemetry payload to all active WS clients
            if connected_clients:
                overview = simulator_instance.get_overview()
                payload = {
                    "type": "telemetry_tick",
                    "overview": overview.model_dump(),
                    "active_alerts_count": overview.active_alerts_count,
                    "facility_health_score": overview.facility_health_score
                }
                serialized = json.dumps(payload)
                
                # Send to all connected sockets
                dead_clients = set()
                for ws in connected_clients:
                    try:
                        await ws.send_text(serialized)
                    except Exception:
                        dead_clients.add(ws)
                connected_clients.difference_update(dead_clients)

            await asyncio.sleep(2.0 / simulator_instance.simulation_speed)
        except asyncio.CancelledError:
            logger.info("Simulation loop received cancellation.")
            break
        except Exception as e:
            logger.error(f"Error in simulation loop: {e}")
            await asyncio.sleep(2.0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        from app.db.seed import seed_database
        seed_database()
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
    sim_task = asyncio.create_task(simulation_background_loop())
    logger.info("FacilityOps Agentic Operating System initialized.")
    yield
    # Shutdown
    sim_task.cancel()
    try:
        await sim_task
    except asyncio.CancelledError:
        pass
    logger.info("FacilityOps shutdown complete.")

app = FastAPI(
    title="Agentic FacilityOps AI Platform",
    description="Intelligent Digital Operating System for Smart Buildings & Industrial Facilities",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local enterprise development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(routes_telemetry.router)
app.include_router(routes_agents.router)
app.include_router(routes_alerts.router)
app.include_router(routes_workorders.router)
app.include_router(routes_simulation.router)
app.include_router(routes_reports.router)
app.include_router(routes_auth.router)

# WebSocket streaming endpoint
@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    logger.info(f"WebSocket client connected. Active connections: {len(connected_clients)}")
    
    # Send initial full overview immediately upon connection
    overview = simulator_instance.get_overview()
    await websocket.send_text(json.dumps({
        "type": "initial_state",
        "overview": overview.model_dump()
    }))
    
    try:
        while True:
            # Keep receiving pings or command messages
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("action") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except Exception:
                pass
    except WebSocketDisconnect:
        connected_clients.discard(websocket)
        logger.info(f"WebSocket client disconnected. Remaining: {len(connected_clients)}")

# Serve Static UI Files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    if (STATIC_DIR / "css").exists():
        app.mount("/css", StaticFiles(directory=str(STATIC_DIR / "css")), name="css")
    if (STATIC_DIR / "js").exists():
        app.mount("/js", StaticFiles(directory=str(STATIC_DIR / "js")), name="js")
    if (STATIC_DIR / "data").exists():
        app.mount("/data", StaticFiles(directory=str(STATIC_DIR / "data")), name="data")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(str(STATIC_DIR / "index.html"))

@app.get("/api/auth/login", include_in_schema=False)
async def login_redirect():
    return RedirectResponse(url="/")
