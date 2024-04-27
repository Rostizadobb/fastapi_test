#from typing import BinaryIO
import io
from azure.storage.blob import BlobServiceClient
import os
from responses_colection.response_json import response_json

AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=azureyellowcab;AccountKey=tlRAtEUmclKrQPupGAnwlo6GyivJyVLI2DzsAlsDxCYbGx1896Jhsr6MOHShABk+ukTMsLSnUclt+AStgk6vww==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_blob(filename: str, container: str, data: io.BytesIO):
    try:
        blob_client = blob_service_client.get_blob_client(container = container, blob = filename)
        blob_client.upload_blob(data, overwrite=True)
        return response_json(message="success")
    except Exception as e:
        return response_json(message=e.message, status = 500)
