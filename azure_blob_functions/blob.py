#from typing import BinaryIO
import io
from azure.storage.blob import BlobServiceClient, BlobType
import os
import uuid
from responses_colection.response_json import response_json

AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=azureyellowcab;AccountKey=tlRAtEUmclKrQPupGAnwlo6GyivJyVLI2DzsAlsDxCYbGx1896Jhsr6MOHShABk+ukTMsLSnUclt+AStgk6vww==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_blob(filename: str, container: str, file):
    try:
        blob_client = blob_service_client.get_blob_client(container = container, blob = filename)
        # upload data
        with file.file as f:
            chunk_size=1024*1024*4
            total_length = 0
            chunks = []
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                chunks.append(chunk)
                total_length += len(chunk)

            for i, chunk in enumerate(chunks):
                blob_client.upload_blob(data=chunk, blob_type=BlobType.BlockBlob, length=total_length)

        # Fetch the blob properties to get the file size
        blob_properties = blob_client.get_blob_properties()
        file_size = blob_properties['size']
        message = f"File uploaded successfully. File size: {file_size} bytes"
        return response_json(message)
    except Exception as e:
        return response_json(message=e.message, status = 500)
            



    #try:
        #blob_client = blob_service_client.get_blob_client(container = container, blob = filename)
        #blob_client.upload_blob(data, overwrite=True)
        #return response_json(message="success")
    #except Exception as e:
        #return response_json(message=e.message, status = 500)
