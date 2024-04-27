from fastapi import APIRouter, Form, UploadFile, File
from azure_blob_functions.blob import upload_blob

blob_routes = APIRouter()

@blob_routes.post("/upload")
async def upload (file: UploadFile = File(...)):
    filename = file.filename
    container = "cabfiles"
    return upload_blob(filename, container, file)