import webbrowser
import threading
import time
import os
import sys
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Get path to bundled frontend (works for both dev and PyInstaller EXE)
if getattr(sys, 'frozen', False):
    # Running as compiled PyInstaller EXE
    base_dir = sys._MEIPASS
    frontend_dir = os.path.join(base_dir, "frontend")
else:
    # Running in normal Python
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

# API Endpoint
@app.get("/api/health")
async def health_check():
    return JSONResponse({"status": "ok", "message": "Server is running!"})

# Serve the frontend index.html
@app.get("/")
async def get_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

# Serve other static files (JS, CSS)
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

def open_browser():
    # Wait a moment for the server to start, then open the browser
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8765")

if __name__ == "__main__":
    # Start the browser opener in a background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start the web server
    print("Starting BeamNG Performance Sim...")
    print("Keep this window open. Close it to quit the app.")
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="error")
