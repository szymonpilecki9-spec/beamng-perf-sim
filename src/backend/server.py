import webbrowser
import threading
import time
import os
import sys
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import beamng_perf_core # Import our C++ module!

app = FastAPI()

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    frontend_dir = os.path.join(base_dir, "frontend")
else:
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

@app.get("/api/health")
async def health_check():
    return JSONResponse({"status": "ok", "message": "Server is running!"})

# NEW: API Endpoint to test C++ math
@app.get("/api/test_cpp")
async def test_cpp():
    # Call the C++ function: calculate torque at 4000 RPM with max torque of 500 Nm
    torque = beamng_perf_core.calculate_torque(4000.0, 500.0)
    return JSONResponse({"rpm": 4000, "torque": torque})

@app.get("/")
async def get_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8765")

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("Starting BeamNG Performance Sim...")
    print("Keep this window open. Close it to quit the app.")
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="error")
