import os
import sys
import json
import time
import asyncio
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Request, Response, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse, FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Smart C&D Waste Routing Platform API",
    description="Real-Time FastAPI for Construction & Demolition Waste Governance & Cross-Dashboard Sync",
    version="2.0.0"
)

# Enable CORS for all frontends & Vercel deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths & File Storage
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_FILE = os.path.join(BASE_DIR, "database.json")

# Master Rosters & System Accounts
SYSTEM_ACCOUNTS = [
    {
        "id": "INS-MCC-183",
        "name": "Gargieee",
        "email": "gat@gmail.com",
        "password": "123",
        "passwords": ["123", "123456"],
        "phone": "+91 98450 11099",
        "role": "inspector",
        "department": "mcc",
        "assignedPin": "501301",
        "assignedArea": "Ward 14 (Palace & City Zone)",
        "designation": "Ward Health Inspector",
        "status": "Active (On Duty)"
    },
    {
        "id": "BOGP1001",
        "name": "Seervi",
        "email": "q@gmail.com",
        "password": "123",
        "passwords": ["123", "123456"],
        "phone": "+91 98450 11002",
        "role": "inspector",
        "department": "gp",
        "assignedPin": "570026",
        "assignedArea": "GP Ward 01 (Bogadi Rural & Ring Road)",
        "designation": "Panchayat Health Inspector",
        "status": "Active (On Duty)"
    },
    {
        "id": "BOGP1002",
        "name": "Dimple",
        "email": "dim@gmail.com",
        "password": "123",
        "passwords": ["123", "123456"],
        "phone": "+91 98450 22003",
        "role": "inspector",
        "department": "gp",
        "assignedPin": "570028",
        "assignedArea": "GP Ward 02 (Maratikyathanahalli Village)",
        "designation": "Village Sanitary Inspector",
        "status": "Active (On Duty)"
    },
    {
        "id": "HTMC1001",
        "name": "M. Anand",
        "email": "anand.tp@gmail.com",
        "password": "123",
        "passwords": ["123", "123456"],
        "phone": "+91 98450 11003",
        "role": "inspector",
        "department": "tp",
        "assignedPin": "570018",
        "assignedArea": "TP Ward 01 (Hootagalli Town & Industrial)",
        "designation": "Town Municipal Inspector",
        "status": "Active (On Duty)"
    },
    {
        "id": "MCCU1001",
        "name": "Rajesh Kumar",
        "email": "inspector.mcc@gmail.com",
        "password": "123",
        "passwords": ["123", "123456"],
        "phone": "+91 98450 11001",
        "role": "inspector",
        "department": "mcc",
        "assignedPin": "570001",
        "assignedArea": "MCC Central & Urban Core",
        "designation": "Ward Health Inspector",
        "status": "Active (On Duty)"
    },
    {
        "id": "OFF-MCC-01",
        "name": "Dr. N. Chandrashekar, IAS",
        "email": "officer.mcc@gmail.com",
        "password": "123",
        "passwords": ["123", "123456"],
        "phone": "+91 98450 11000",
        "role": "officer",
        "department": "mcc",
        "designation": "Municipal Commissioner",
        "status": "Active (On Duty)"
    },
    {
        "id": "OFF-GP-01",
        "name": "K. S. Manjunath",
        "email": "gp@gmail.com",
        "password": "123",
        "passwords": ["123", "123456"],
        "phone": "+91 98450 22000",
        "role": "officer",
        "department": "gp",
        "designation": "Panchayat Development Officer",
        "status": "Active (On Duty)"
    },
    {
        "id": "OFF-TP-01",
        "name": "S. Ramesh",
        "email": "tp@gmail.com",
        "password": "123",
        "passwords": ["123", "123456"],
        "phone": "+91 98450 33000",
        "role": "officer",
        "department": "tp",
        "designation": "Chief Officer / Zonal Superintendent",
        "status": "Active (On Duty)"
    }
]

# In-Memory Cache for fast execution
memory_db = {
    "stats": {
        "totalApplications": 0,
        "pendingInspections": 0,
        "pendingDebris": 0,
        "completedCollections": 0,
        "activeOfficers": 3,
        "totalTonnageCollected": "0 MT",
        "recyclingEfficiency": "100%"
    },
    "applications": [],
    "registeredUsers": list(SYSTEM_ACCOUNTS)
}

CLOUD_APP_OBJECT_ID = "ff808181a09d98f701a11a6b828e1e21"
CLOUD_USER_OBJECT_ID = "ff808181a09d98f701a0b5665eda376f"

def fetch_cloud_apps():
    try:
        res = requests.get(f"https://api.restful-api.dev/objects/{CLOUD_APP_OBJECT_ID}", headers={"User-Agent": "FastAPI"}, timeout=3)
        if res.status_code == 200:
            d = res.json().get("data", {})
            return d.get("applications", []), d.get("stats", None)
    except Exception:
        pass
    return None, None

def persist_cloud_apps(apps, stats):
    try:
        clean_apps = apps[:100]
        payload = {"data": {"applications": clean_apps, "stats": stats}}
        requests.patch(f"https://api.restful-api.dev/objects/{CLOUD_APP_OBJECT_ID}", json=payload, headers={"User-Agent": "FastAPI"}, timeout=3)
    except Exception:
        pass

def fetch_cloud_users():
    try:
        res = requests.get(f"https://api.restful-api.dev/objects/{CLOUD_USER_OBJECT_ID}", headers={"User-Agent": "FastAPI"}, timeout=3)
        if res.status_code == 200:
            return res.json().get("data", {}).get("users", [])
    except Exception:
        pass
    return []

def persist_cloud_users(users):
    try:
        payload = {"data": {"users": users}}
        requests.patch(f"https://api.restful-api.dev/objects/{CLOUD_USER_OBJECT_ID}", json=payload, headers={"User-Agent": "FastAPI"}, timeout=3)
    except Exception:
        pass

def get_storage_path():
    parent = os.path.dirname(DATA_FILE)
    if os.path.exists(parent) and os.access(parent, os.W_OK):
        return DATA_FILE
    return "/tmp/database.json"

def load_data():
    global memory_db
    p = get_storage_path()
    if not os.path.exists(p) and os.path.exists(DATA_FILE):
        p = DATA_FILE
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    memory_db["stats"] = data.get("stats", memory_db["stats"])
                    memory_db["applications"] = data.get("applications", [])
                    if "registeredUsers" in data:
                        memory_db["registeredUsers"] = data.get("registeredUsers", memory_db["registeredUsers"])
        except Exception:
            pass

    # Merge with Cloud Object Store
    try:
        c_apps, c_stats = fetch_cloud_apps()
        if c_apps:
            existing_ids = {a.get("id") for a in memory_db["applications"] if a.get("id")}
            for ca in c_apps:
                if ca.get("id") not in existing_ids:
                    memory_db["applications"].append(ca)
                    existing_ids.add(ca.get("id"))
            if c_stats:
                memory_db["stats"].update(c_stats)
    except Exception:
        pass

    try:
        c_users = fetch_cloud_users()
        existing_emails = {str(u.get("email", "")).lower() for u in memory_db["registeredUsers"]}
        for cu in c_users:
            if str(cu.get("email", "")).lower() not in existing_emails:
                memory_db["registeredUsers"].append(cu)
                existing_emails.add(str(cu.get("email", "")).lower())
    except Exception:
        pass

def save_data():
    try:
        data_to_save = {
            "stats": memory_db["stats"],
            "applications": memory_db["applications"],
            "registeredUsers": memory_db["registeredUsers"],
            "hotspots": []
        }
        target = get_storage_path()
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2)
    except Exception:
        pass

load_data()

# Real-Time SSE (Server-Sent Events) Pub/Sub Queue
subscribers: List[asyncio.Queue] = []

async def broadcast_event(event_type: str, payload: Any):
    msg = json.dumps({"type": event_type, "data": payload, "timestamp": time.time()})
    for q in list(subscribers):
        try:
            await q.put(msg)
        except Exception:
            if q in subscribers:
                subscribers.remove(q)

@app.get("/api/stream")
async def event_stream(request: Request):
    """Real-Time Server-Sent Events (SSE) Stream for Dashboard-to-Dashboard Instant Updates"""
    q = asyncio.Queue()
    subscribers.append(q)

    async def event_generator():
        try:
            yield f"data: {json.dumps({'type': 'connected', 'timestamp': time.time()})}\n\n"
            while True:
                if await request.is_disconnected():
                    break
                try:
                    data = await asyncio.wait_for(q.get(), timeout=12.0)
                    yield f"data: {data}\n\n"
                except asyncio.TimeoutError:
                    yield f": heartbeat\n\n"
        finally:
            if q in subscribers:
                subscribers.remove(q)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

# Models
class ApplicationCreate(BaseModel):
    id: Optional[str] = None
    applicantName: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    pincode: Optional[str] = None
    pin: Optional[str] = None
    address: Optional[str] = None
    propertyId: Optional[str] = None
    propertyType: Optional[str] = "Residential"
    material: Optional[str] = "Concrete & Rubble"
    tonnage: Optional[float] = 10.0
    status: Optional[str] = "Pending Inspection"
    lat: Optional[float] = None
    lng: Optional[float] = None
    gpsLocation: Optional[str] = None
    mapUrl: Optional[str] = None
    photos: Optional[List[str]] = []
    photo: Optional[str] = None
    authorityKey: Optional[str] = None
    authority: Optional[str] = None
    assignedInspectorName: Optional[str] = None
    assignedInspectorEmail: Optional[str] = None
    assignedOfficerEmail: Optional[str] = None
    certificateNo: Optional[str] = None
    scheduledDate: Optional[str] = None
    completionDate: Optional[str] = None
    notes: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

# PIN Routing Resolver
def resolve_pin_routing(pin: str):
    clean_pin = str(pin or "").strip()
    
    # 1. Custom PINs
    if clean_pin == "501301":
        return {
            "authorityKey": "mcc",
            "authority": "Mysuru Municipal Corporation (MCC Urban)",
            "assignedOfficerEmail": "officer.mcc@gmail.com",
            "assignedInspectorName": "Gargieee",
            "assignedInspectorEmail": "gat@gmail.com"
        }

    # 2. Check dynamic registered inspectors
    all_users = list(memory_db.get("registeredUsers", [])) + list(SYSTEM_ACCOUNTS)
    for ins in all_users:
        if ins and ins.get("role") == "inspector":
            ins_pin = str(ins.get("assignedPin") or ins.get("pin") or "").strip()
            if ins_pin:
                p_list = [p.strip() for p in ins_pin.replace(",", " ").split() if p.strip()]
                if any(p == clean_pin or clean_pin.startswith(p) or p.startswith(clean_pin) for p in p_list):
                    dept = (ins.get("department") or "").lower()
                    dept_name = (ins.get("departmentName") or "").lower()
                    auth_key = "mcc"
                    auth_name = "Mysuru Municipal Corporation (MCC Urban)"
                    off_email = "officer.mcc@gmail.com"
                    if "gp" in dept or "panchayat" in dept or "panchayat" in dept_name:
                        auth_key = "gp"
                        auth_name = "Bogadi Gram Panchayat (Rural)"
                        off_email = "gp@gmail.com"
                    elif "tp" in dept or "town" in dept or "town" in dept_name:
                        auth_key = "tp"
                        auth_name = "Hootagalli Town Panchayat"
                        off_email = "tp@gmail.com"
                    return {
                        "authorityKey": auth_key,
                        "authority": auth_name,
                        "assignedOfficerEmail": off_email,
                        "assignedInspectorName": ins.get("name"),
                        "assignedInspectorEmail": ins.get("email")
                    }

    GP_PINS = ['570026', '571130', '570028', '560079', '570021', '571311', '571201', '571186', '571101', '571120', '571124', '571125']
    TP_PINS = ['570018', '570017', '570027', '571607', '571604', '571602', '571610', '570016']

    is_gp = any(clean_pin.startswith(p) or p.startswith(clean_pin) or clean_pin == p for p in GP_PINS)
    is_tp = any(clean_pin.startswith(p) or p.startswith(clean_pin) or clean_pin == p for p in TP_PINS)

    if is_gp:
        insp_name = "Seervi"
        insp_email = "q@gmail.com"
        if clean_pin == "570028":
            insp_name = "Dimple"
            insp_email = "dim@gmail.com"
        elif clean_pin == "571130":
            insp_name = "Basavarajappa M."
            insp_email = "basava.gp@gmail.com"
        elif clean_pin == "571311":
            insp_name = "S. Nanjappa"
            insp_email = "nanjappa.gp@gmail.com"
        return {
            "authorityKey": "gp",
            "authority": "Bogadi Gram Panchayat (Rural)",
            "assignedOfficerEmail": "gp@gmail.com",
            "assignedInspectorName": insp_name,
            "assignedInspectorEmail": insp_email
        }
    elif is_tp:
        insp_name = "M. Anand"
        insp_email = "anand.tp@gmail.com"
        if clean_pin == "570017":
            insp_name = "Manjunatha Rao"
            insp_email = "manju.tp@gmail.com"
        elif clean_pin == "570027":
            insp_name = "Prashanth G."
            insp_email = "prashanth.tp@gmail.com"
        return {
            "authorityKey": "tp",
            "authority": "Hootagalli Town Panchayat",
            "assignedOfficerEmail": "tp@gmail.com",
            "assignedInspectorName": insp_name,
            "assignedInspectorEmail": insp_email
        }
    else:
        insp_name = "Rajesh Kumar"
        insp_email = "inspector.mcc@gmail.com"
        if clean_pin == "570002":
            insp_name = "S. Swamy"
            insp_email = "swamy.mcc@gmail.com"
        elif clean_pin == "570004":
            insp_name = "Divya Shankar"
            insp_email = "divya.mcc@gmail.com"
        elif clean_pin == "570023":
            insp_name = "P. Ramesh"
            insp_email = "ramesh.mcc@gmail.com"
        return {
            "authorityKey": "mcc",
            "authority": "Mysuru Municipal Corporation (MCC Urban)",
            "assignedOfficerEmail": "officer.mcc@gmail.com",
            "assignedInspectorName": insp_name,
            "assignedInspectorEmail": insp_email
        }

# API Endpoints
@app.get("/api/applications")
async def get_applications(authority: Optional[str] = None, inspector: Optional[str] = None):
    load_data()
    apps = memory_db.get("applications", [])
    if authority:
        apps = [a for a in apps if (a.get("authorityKey") or "").lower() == authority.lower()]
    if inspector:
        apps = [a for a in apps if (a.get("assignedInspectorEmail") or "").lower() == inspector.lower()]
    return apps

@app.post("/api/applications")
async def create_application(app_data: ApplicationCreate):
    app_dict = app_data.dict()
    
    # Generate ID if missing
    pin = app_dict.get("pincode") or app_dict.get("pin") or "570001"
    routing = resolve_pin_routing(pin)
    
    if not app_dict.get("id"):
        prefix = "#" + routing["authorityKey"].upper() + str(time.strftime("%Y"))
        app_dict["id"] = prefix + str(int(time.time() * 1000))[-6:]
    
    if not app_dict.get("authorityKey"):
        app_dict["authorityKey"] = routing["authorityKey"]
        app_dict["authority"] = routing["authority"]
        app_dict["assignedOfficerEmail"] = routing["assignedOfficerEmail"]
        app_dict["assignedInspectorName"] = routing["assignedInspectorName"]
        app_dict["assignedInspectorEmail"] = routing["assignedInspectorEmail"]
    
    app_dict["submittedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    
    # Prepend to memory applications
    memory_db["applications"].insert(0, app_dict)
    memory_db["stats"]["totalApplications"] = len(memory_db["applications"])
    memory_db["stats"]["pendingInspections"] = sum(1 for a in memory_db["applications"] if a.get("status") in ["Pending Inspection", "Pending Verification"])
    save_data()
    persist_cloud_apps(memory_db["applications"], memory_db["stats"])

    # REAL-TIME BROADCAST: Instant Push to Inspector & Officer Dashboards
    await broadcast_event("NEW_APPLICATION", app_dict)

    return {"success": True, "application": app_dict, "id": app_dict["id"], "item": app_dict}

@app.patch("/api/applications/{app_id}")
@app.post("/api/applications/update")
async def update_application(app_id: Optional[str] = None, req: Request = None):
    body = await req.json()
    target_id = app_id or body.get("id") or body.get("requestId")
    if not target_id:
        raise HTTPException(status_code=400, detail="Application ID is required")

    found = None
    for a in memory_db["applications"]:
        if str(a.get("id")) == str(target_id):
            a.update(body)
            found = a
            break

    if not found:
        # Append if new
        found = body
        found["id"] = target_id
        memory_db["applications"].insert(0, found)

    save_data()
    persist_cloud_apps(memory_db["applications"], memory_db["stats"])

    # REAL-TIME BROADCAST: Instant Push to All Dashboards
    await broadcast_event("APPLICATION_UPDATED", found)

    return {"success": True, "application": found, "item": found}

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    load_data()
    total = len(memory_db.get("applications", []))
    pending = sum(1 for a in memory_db.get("applications", []) if a.get("status") in ["Pending Inspection", "Pending Verification"])
    completed = sum(1 for a in memory_db.get("applications", []) if a.get("status") in ["Approved", "Clearance Approved", "Issued"])
    memory_db["stats"]["totalApplications"] = total
    memory_db["stats"]["pendingInspections"] = pending
    memory_db["stats"]["completedCollections"] = completed
    return {
        "stats": memory_db["stats"],
        "hotspots": []
    }

@app.get("/api/auth/users")
async def get_auth_users():
    load_data()
    # Return unique merged list of system accounts and registered users
    combined = list(SYSTEM_ACCOUNTS)
    seen = {str(u.get("email", "")).lower() for u in combined}
    for u in memory_db.get("registeredUsers", []):
        em = str(u.get("email", "")).lower()
        if em and em not in seen:
            combined.append(u)
            seen.add(em)
    return combined

@app.post("/api/auth/register")
async def auth_register(req: Request):
    body = await req.json()
    email = str(body.get("email") or "").strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    found_idx = -1
    for idx, u in enumerate(memory_db["registeredUsers"]):
        if str(u.get("email") or "").strip().lower() == email:
            found_idx = idx
            break

    new_user = dict(body)
    new_user["email"] = email
    if not new_user.get("id"):
        new_user["id"] = "u_" + str(int(time.time() * 1000))

    if found_idx >= 0:
        memory_db["registeredUsers"][found_idx].update(new_user)
        ret_user = memory_db["registeredUsers"][found_idx]
    else:
        memory_db["registeredUsers"].append(new_user)
        ret_user = new_user

    save_data()
    persist_cloud_users(memory_db["registeredUsers"])
    return {"success": True, "user": ret_user}

@app.post("/api/auth/login")
async def auth_login(login: LoginRequest):
    email = login.email.strip().lower()
    pw = login.password.strip()

    all_users = list(memory_db.get("registeredUsers", [])) + list(SYSTEM_ACCOUNTS)
    for u in all_users:
        if (u.get("email") or "").lower() == email:
            valid_passwords = u.get("passwords", [u.get("password")])
            if pw in valid_passwords or pw == u.get("password"):
                return {"success": True, "user": u}

    # Citizen dynamic fallback login
    return {
        "success": True,
        "user": {
            "name": email.split("@")[0].capitalize(),
            "email": email,
            "role": "citizen"
        }
    }

@app.get("/api/reverse-geocode")
async def reverse_geocode(lat: float, lng: float):
    """High-accuracy reverse geocoding via OpenStreetMap with custom User-Agent"""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lng}&format=json&addressdetails=1"
        headers = {
            "User-Agent": "CivicTrack-Mysuru/2.0 (contact@civictrack.org)",
            "Accept-Language": "en"
        }
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            addr = data.get("address", {})
            postcode = str(addr.get("postcode", "")).replace(" ", "")[:6]
            road = addr.get("road") or addr.get("street") or addr.get("suburb") or addr.get("neighbourhood") or ""
            locality = addr.get("suburb") or addr.get("village") or addr.get("town") or addr.get("city_district") or addr.get("city") or ""
            city = addr.get("city") or addr.get("state_district") or addr.get("county") or ""
            full_address = ", ".join(filter(None, [road, locality, city])) or data.get("display_name", "")
            return {
                "success": True,
                "postcode": postcode,
                "fullAddress": full_address,
                "displayName": data.get("display_name", full_address),
                "lat": lat,
                "lng": lng
            }
    except Exception as e:
        pass
    
    return {
        "success": False,
        "postcode": "570001",
        "fullAddress": "Sayyaji Rao Road, Devaraja Mohalla, Mysuru",
        "lat": lat,
        "lng": lng
    }

# HTML Page Routes (Serve frontend portals directly)
@app.get("/")
@app.get("/index.html")
async def serve_index():
    path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(path):
        return FileResponse(path)
    return FileResponse(os.path.join(BASE_DIR, "citizen.html"))

@app.get("/citizen.html")
async def serve_citizen():
    return FileResponse(os.path.join(BASE_DIR, "citizen.html"))

@app.get("/inspector.html")
async def serve_inspector():
    return FileResponse(os.path.join(BASE_DIR, "inspector.html"))

@app.get("/officer.html")
async def serve_officer():
    return FileResponse(os.path.join(BASE_DIR, "officer.html"))

@app.get("/dashboard.html")
async def serve_dashboard():
    return FileResponse(os.path.join(BASE_DIR, "dashboard.html"))

@app.get("/auth.html")
async def serve_auth():
    return FileResponse(os.path.join(BASE_DIR, "auth.html"))

@app.get("/{filename}.js")
async def serve_js(filename: str):
    p = os.path.join(BASE_DIR, f"{filename}.js")
    if os.path.exists(p):
        return FileResponse(p, media_type="application/javascript")
    raise HTTPException(status_code=404)

assets_dir = os.path.join(BASE_DIR, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

