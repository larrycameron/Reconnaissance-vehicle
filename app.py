import os
import json
from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.security.api_key import APIKeyHeader
from typing import Optional

app = FastAPI(title="Vehicle Standalone Dashboard")

# Config
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../roadmesh'))
STATUS_FILE = os.path.join(DATA_DIR, 'vehicle_status.json')
LOG_FILE = os.path.join(DATA_DIR, 'vehicle_logs.txt')
COMMAND_FILE = os.path.join(DATA_DIR, 'vehicle_commands.json')
SNAPSHOT_FILE = os.path.join(DATA_DIR, 'latest_image.jpg')
API_KEY = "changemeapikey"  # Change for production
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key_header: Optional[str] = Depends(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key_header

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <html><head><title>Vehicle Dashboard</title></head><body>
    <h1>Vehicle Dashboard</h1>
    <div id='status'></div>
    <button onclick="fetch('/status').then(r=>r.json()).then(d=>document.getElementById('status').innerText=JSON.stringify(d,null,2))">Refresh Status</button>
    <form method='post' action='/control/start'><button type='submit'>Start Vehicle</button></form>
    <form method='post' action='/control/stop'><button type='submit'>Stop Vehicle</button></form>
    <form method='post' action='/control/manual'>
      <input name='direction' placeholder='Direction'>
      <input name='speed' placeholder='Speed'>
      <button type='submit'>Manual Control</button>
    </form>
    <a href='/logs'>View Logs</a><br>
    <a href='/camera/snapshot'>Latest Camera Snapshot</a>
    </body></html>
    """

@app.get("/status")
def get_status():
    if not os.path.exists(STATUS_FILE):
        return {"error": "No status available"}
    with open(STATUS_FILE) as f:
        return json.load(f)

@app.get("/logs")
def get_logs():
    if not os.path.exists(LOG_FILE):
        return {"logs": []}
    with open(LOG_FILE) as f:
        logs = f.readlines()
    return {"logs": logs[-100:]}

@app.post("/control/start")
def start_vehicle(api_key: str = Depends(get_api_key)):
    _write_command({"action": "start"})
    return {"result": "Vehicle start command sent"}

@app.post("/control/stop")
def stop_vehicle(api_key: str = Depends(get_api_key)):
    _write_command({"action": "stop"})
    return {"result": "Vehicle stop command sent"}

@app.post("/control/manual")
def manual_control(direction: str = Form(...), speed: str = Form(...), api_key: str = Depends(get_api_key)):
    _write_command({"action": "manual", "direction": direction, "speed": speed})
    return {"result": f"Manual control: {direction} at {speed}"}

@app.get("/camera/snapshot")
def camera_snapshot():
    if not os.path.exists(SNAPSHOT_FILE):
        return JSONResponse({"error": "No snapshot available"}, status_code=404)
    return FileResponse(SNAPSHOT_FILE, media_type="image/jpeg")

def _write_command(cmd):
    # Append command to command file (as a list of commands)
    commands = []
    if os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE) as f:
            try:
                commands = json.load(f)
            except Exception:
                commands = []
    commands.append(cmd)
    with open(COMMAND_FILE, 'w') as f:
        json.dump(commands, f) 