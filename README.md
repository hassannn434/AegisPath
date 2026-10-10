# 🛡️ AegisPath: Safety-Oriented Navigation & Emergency Sentinel Engine

**AegisPath** is a production-grade, low-latency backend application built with **FastAPI** designed for live route monitoring, geospatial drift detection, and automated emergency SOS dispatching.

---

## 👨‍💻 Author
* **Hassan Mahadkar**
* **GitHub:** [@hassannn434](https://github.com/hassannn434)
* **Repository:** [AegisPath](https://github.com/hassannn434/AegisPath)

---

## 🎯 Problem Statement & Solution

Traditional navigation systems focus on calculating the fastest route, often ignoring live user safety deviations or instant emergency detection mechanisms. **AegisPath** addresses this by providing two real-time safety services:
1. **Continuous Geospatial Route Monitoring:** Verifies live GPS updates against a safe corridor using mathematical distance formulas.
2. **Panic Gesture Emergency Sentinel:** Intercepts real-time phone accelerometer telemetry to detect high-acceleration shake patterns and automatically trigger an emergency broadcast.

---

## 🛠️ Complete Tech Stack

* **Framework:** FastAPI (Asynchronous Python Web Framework)
* **Language:** Python 3.10+
* **Data Validation & Schemas:** Pydantic (Type safety & JSON parsing)
* **ASGI Web Server:** Uvicorn (Running on port `8001`)
* **Geospatial Processing:** Math module (Haversine Formula)
* **API Documentation & Testing:** Swagger UI / OpenAPI 3.1 (`/docs`)

---

## 🏗️ Architecture & Core Components

AegisPath/
├── backend_api.py         # Primary FastAPI application, REST endpoints & Uvicorn launcher
├── emergency_handler.py   # EmergencySentinel class & panic gesture detection logic
├── requirements.txt       # Project dependencies (FastAPI, Uvicorn, Pydantic)
└── README.md              # Detailed project documentation & live demo guide


---

### 1. Data Flow & System Execution Architecture

[ Mobile Telemetry / Client ]
│
├──► POST /api/v1/monitor/ping ──────► [ Haversine Engine ] ──► [ Corridor Drift Alert ]
│
└──► POST /api/v1/emergency/shake-trigger ─► [ EmergencySentinel ] ──► [ Structured SOS Payload ]


---

### 2. Deep Dive into Core Modules

#### A. The Geospatial Drift Engine (`backend_api.py`)
* **Mathematical Foundation:** Employs the **Haversine Formula** to compute the great-circle distance between two latitude/longitude points on a sphere:
  $$d = 2R \cdot \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)}\right)$$
* **Real-Time Validation:** Receives telemetry pings via `GPSCoordinate` Pydantic model and compares the current user position against a designated target corridor radius (`100.0 meters`).
* **Automated Flagging:** Triggers a route departure warning immediately upon threshold violation.

#### B. The Emergency Sentinel Engine (`emergency_handler.py`)
* **Gesture Detection:** Evaluates $3D$ accelerometer vector magnitude ($\sqrt{x^2 + y^2 + z^2}$) against a calibrated shake threshold (`15.0 m/s²`).
* **Payload Generation:** Upon detecting high-acceleration panic gestures, the sentinel dynamically construct an SOS payload featuring:
  * Standard ISO/Timestamp logging.
  * Direct Google Maps deep-link generation (`https://maps.google.com/?q=lat,lon`).
  * Automated emergency message formatting directed to trusted contacts.

#### C. Request Validation & Type Safety
* **Pydantic Schemas:** Enforces strict data models (`GPSCoordinate`, `AccelerometerData`) at runtime, preventing malformed payloads from penetrating internal calculation engines.
* **OpenAPI Schema Generation:** Automatically generates interactive documentation (`/docs`) and schema definitions via Swagger UI.

 ### Live Demo and output
 Live Demo Link- http://127.0.0.1:8001/docs

 Screenshots -
 <img width="1914" height="850" alt="image" src="https://github.com/user-attachments/assets/b8dad479-69b3-4d80-8b7e-6025183b0eea" />
 <img width="1919" height="803" alt="image" src="https://github.com/user-attachments/assets/7b4f291e-4748-4a8e-a906-bb7749e9e5c9" />
<img width="1901" height="912" alt="image" src="https://github.com/user-attachments/assets/0c4b68f9-7d13-47f1-95e1-80e8141c7b36" />
<img width="1900" height="905" alt="image" src="https://github.com/user-attachments/assets/5bb14380-6674-41a1-8716-62adaaa53b80" />



## 📌 Conclusion & Future Roadmap

**AegisPath** demonstrates how lightweight, asynchronous Python architectures can be leveraged to build responsive, life-saving navigation logic. By combining mathematical geospatial analysis with real-time hardware telemetry parsing, the engine provides an effective framework for proactive safety monitoring.

### 🚀 Future Enhancements
* **WebSockets Integration:** Transition from polling telemetry pings to full-duplex WebSocket channels for sub-millisecond route tracking.
* **Database Persistence:** Integrate PostgreSQL/PostGIS for storing spatial route corridors and historical telemetry logs.
* **Twilio/SMS API Integration:** Connect live SMS gateway dispatches for automated cellular broadcasts during emergency triggers.
* **Geofencing Engine:** Expand beyond corridor offsets to include dynamic polygon-based safe/unsafe zone evaluations.

---


## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
