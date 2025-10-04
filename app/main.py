import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from filelock import FileLock

app = FastAPI(title="Counter API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "/data/counter.json"
LOCK_FILE = "/data/counter.lock"


def read_counter():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("value", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def write_counter(value):
    with open(DATA_FILE, "w") as f:
        json.dump({"value": value}, f)

@app.get("/counter")
def get_counter():
    with FileLock(LOCK_FILE):
        current_value = read_counter()
    return {"counter": current_value}

@app.post("/increment")
def increment_counter():
    with FileLock(LOCK_FILE):
        current_value = read_counter()
        new_value = current_value + 1
        write_counter(new_value)
    return {"counter": new_value}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        write_counter(0)
