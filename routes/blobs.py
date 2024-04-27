from fastapi import APIRouter, Form, UploadFile, File
from azure_blob_functions.blob import upload_blob
import io

from azure.storage.blob import BlobServiceClient
from responses_colection.response_json import response_json
blob_routes = APIRouter()
AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=azureyellowcab;AccountKey=tlRAtEUmclKrQPupGAnwlo6GyivJyVLI2DzsAlsDxCYbGx1896Jhsr6MOHShABk+ukTMsLSnUclt+AStgk6vww==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

@blob_routes.post("/upload")
async def upload (container: str = Form(...), file: UploadFile = File(...)):
    data = await file.read()
    bytes_io = io.BytesIO(data)
    filename = file.filename
    return upload_blob(filename, container, bytes_io)

@blob_routes.post("/uploadnew")
async def upload(container: str = Form(...), file: UploadFile = File(...)):
    try:
        # Generate a unique name for the blob using the file's name
        filename = file.filename
        blob_client = blob_service_client.get_blob_client(container=container, blob=filename)
        
        # Upload the file in chunks
        with file.file as stream:
            chunk_size = 4 * 1024 * 1024  # 4MB chunk size (adjust as needed)
            index = 0
            while True:
                chunk = stream.read(chunk_size)
                if not chunk:
                    break
                blob_client.upload_blob(chunk, blob_type="BlockBlob", length=len(chunk), blob_offset=index)
                index += len(chunk)
        
        return response_json(message="success")
    except Exception as e:
        return response_json(message=str(e), status=500)
