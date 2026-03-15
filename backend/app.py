"""
AlgoVision — Backend API
FastAPI application serving step-by-step algorithm visualization data.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# ── Resolve base directory (works in normal mode and PyInstaller EXE) ──
if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle
    BASE_DIR = sys._MEIPASS
else:
    # Running normally — backend/ is the working directory
    BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

app = FastAPI(
    title="AlgoVision API",
    description="Step-by-step algorithm visualization backend",
    version="2.0.0",
)

# ── CORS: allow frontend to call API ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register route modules ──
from routes.sorting_routes import router as sorting_router
from routes.graph_routes import router as graph_router
from routes.tree_routes import router as tree_router
from routes.geometry_routes import router as geometry_router

app.include_router(sorting_router)
app.include_router(graph_router)
app.include_router(tree_router)
app.include_router(geometry_router)


# ── Health check ──
@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0", "algorithms": 113}


# ── Shutdown ──
import threading

@app.post("/shutdown")
async def shutdown():
    """Shut down the server cleanly. Works on Windows + Linux."""
    def _kill():
        import time
        time.sleep(0.5)
        os._exit(0)
    threading.Thread(target=_kill, daemon=True).start()
    return {"status": "shutting down"}


# ── Algorithm Registry ──
import json

REGISTRY_PATH = os.path.join(BASE_DIR, "shared", "algorithm_registry.json")

@app.get("/registry")
async def get_registry():
    if os.path.isfile(REGISTRY_PATH):
        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)
    return {"error": "Registry not found"}


# ── Serve frontend ──
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if os.path.isdir(FRONTEND_DIR):
    for subdir in ["css", "js", "assets"]:
        subdir_path = os.path.join(FRONTEND_DIR, subdir)
        if os.path.isdir(subdir_path):
            app.mount(f"/{subdir}", StaticFiles(directory=subdir_path), name=subdir)

    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# ── Startup ──
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
