from fastapi import FastAPI
from routes.blobs import blob_routes

app = FastAPI()
app.include_router(blob_routes, prefix= "/cabfiles")

@app.get("/info")
def info():
    return {"name": "ob-sample-fast-api", "version": "1.0.0"}
