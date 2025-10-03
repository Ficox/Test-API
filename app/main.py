from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Counter API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

counter = {"value": 0}

@app.get("/counter")
def get_counter():
    return {"counter": counter["value"]}

@app.post("/increment")
def increment_counter():
    counter["value"] += 1
    return {"counter": counter["value"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}
