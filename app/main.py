from fastapi import FastApi

app = FastAPI()

@app.get("/info")
def info():
    return {"name": "ob-sample-fast-api", "version": "1.0.0"}