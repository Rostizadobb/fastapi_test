from fastapi import APIRouter, Form, UploadFile, File
from azure_blob_functions.blob import upload_blob
import io

blob_routes = APIRouter()

@blob_routes.post("/upload")
async def upload (container: str = Form(...), file: UploadFile = File(...)):
    data = await file.read()
    bytes_io = io.BytesIO(data)
    filename = file.filename
    return upload_blob(filename, container, bytes_io)