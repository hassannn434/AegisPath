from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math
from emergency_handler import EmergencySentinel

app = FastAPI(title="AegisPath Safety & Emergency Engine", version="1.1")

# Initialize emergency sentinel with a shake sensitivity threshold
sentinel = EmergencySentinel(shake_threshold=15.0)

# Request Models
class GPSCoordinate(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    trip_id: str

class AccelerometerData(BaseModel):
    user_id: str
    x_axis: float
    y_axis: float
    z_axis: float
    latitude: float
    longitude: float
    trusted_contact: str

# Simulated safe corridor center coordinates
TARGET_CORRIDOR = {"lat_center": 19.0760, "lon_center": 72.8777, "max_allowed_drift_meters": 100.0}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

@app.get("/")
def read_root():
    return {
        "project": "AegisPath Safety & Emergency Engine",
        "status": "Active",
        "documentation_url": "/docs"
    }

@app.post("/api/v1/monitor/ping")
def monitor_user_location(coord: GPSCoordinate):
    """
    Drift Monitor Agent Endpoint: Checks live GPS coordinates against the secure route corridor.
    """
    distance_from_corridor = haversine_distance(
        coord.latitude, coord.longitude,
        TARGET_CORRIDOR["lat_center"], TARGET_CORRIDOR["lon_center"]
    )
    
    status = "Normal"
    alert_triggered = False
    
    if distance_from_corridor > TARGET_CORRIDOR["max_allowed_drift_meters"]:
        status = "Warning: Route Drift Detected"
        alert_triggered = True
        
    return {
        "trip_id": coord.trip_id,
        "status": status,
        "distance_offset_meters": round(distance_from_corridor, 2),
        "alert_triggered": alert_triggered,
        "message": "Drift Monitor Agent active. Safe corridor intact." if not alert_triggered else "⚠️ Warning: User has drifted outside the secure corridor."
    }

@app.post("/api/v1/emergency/shake-trigger")
def handle_shake_trigger(data: AccelerometerData):
    """
    Emergency Sentinel Endpoint: Evaluates phone accelerometer readings for panic shake patterns.
    """
    is_shake_detected = sentinel.evaluate_accelerometer(data.x_axis, data.y_axis, data.z_axis)
    
    if is_shake_detected:
        sos_response = sentinel.trigger_sos_workflow(
            user_id=data.user_id,
            latitude=data.latitude,
            longitude=data.longitude,
            trusted_contact=data.trusted_contact
        )
        return {
            "success": True,
            "alert_status": "SOS Broadcasted Successfully",
            "details": sos_response
        }
    
    return {
        "success": True,
        "alert_status": "Normal",
        "message": "Accelerometer readings within normal range. No shake pattern detected."
    }

# Startup block configured to run on port 8001
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)