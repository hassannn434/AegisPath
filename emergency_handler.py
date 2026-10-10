import math
from datetime import datetime

class EmergencySentinel:
    def __init__(self, shake_threshold=2.5):
        # Acceleration threshold in G-forces or m/s² delta indicating a panic shake
        self.shake_threshold = shake_threshold

    def evaluate_accelerometer(self, x: float, y: float, z: float) -> bool:
        """
        Calculates total vector magnitude from phone accelerometer (X, Y, Z axes).
        Standard gravity is ~9.8 m/s². A sudden spike indicates a shake event.
        """
        total_acceleration = math.sqrt(x**2 + y**2 + z**2)
        
        # Check if acceleration exceeds normal baseline movement threshold
        if total_acceleration > self.shake_threshold:
            return True
        return False

    def trigger_sos_workflow(self, user_id: str, latitude: float, longitude: float, trusted_contact: str):
        """
        Compiles the emergency payload and triggers automated alert broadcast[cite: 1].
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        alert_payload = {
            "status": "EMERGENCY_TRIGGERED",
            "trigger_type": "SHAKE_ACCELEROMETER",
            "user_id": user_id,
            "timestamp": timestamp,
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "google_maps_link": f"https://maps.google.com/?q={latitude},{longitude}"
            },
            "dispatched_to": trusted_contact,
            "message": "🚨 URGENT: AegisPath Emergency Sentinel activated via shake gesture. Live coordinates attached."
        }
        
        # In a production environment, this would interface with an SMS API (e.g., Twilio)
        print(f"[ALERT DISPATCHED] -> Broadcasting to {trusted_contact} at {timestamp}")
        return alert_payload