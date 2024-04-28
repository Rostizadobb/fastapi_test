from azure_blob_functions.blob import upload_blob
import io
from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd


blob_routes = APIRouter()

@blob_routes.post("/upload")
async def upload (file: UploadFile = File(...)):
    if not file.filename.endswith(".parquet"):
        raise HTTPException(status_code=400, detail="Uploaded file must be in .parquet format")
    parquet_data = pd.read_parquet(io.BytesIO(await file.read()))
    csv_data = parquet_data.to_csv(index=False)
    converted_file = io.BytesIO(csv_data.encode())
    csv_file = UploadFile(filename=file.filename.replace(".parquet", ".csv"), file=converted_file, media_type="text/csv")
    filename = csv_file.filename
    return upload_blob(filename, csv_file)