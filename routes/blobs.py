from azure_blob_functions.blob import upload_blob
from fastapi import APIRouter, UploadFile, File, HTTPException


blob_routes = APIRouter()

@blob_routes.post("/upload")
async def upload (file: UploadFile = File(...)):
    if not file.filename.endswith(".parquet"):
        raise HTTPException(status_code=400, detail="Uploaded file must be in .parquet format")
    filename = file.filename
    return upload_blob(filename, file)