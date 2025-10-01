from fastapi import FastAPI

app = FastAPI(title="FastAPI GHCR Example")

@app.get("/")
def read_root():
    return {"ok": True, "service": "fastapi-ghcr-example"}

@app.get("/health")
def health():
    return {"status": "healthy"}
