#from typing import BinaryIO
import io
from azure.storage.blob import BlobServiceClient, BlobBlock
import os
import uuid
from responses_colection.response_json import response_json

AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=azureyellowcab;AccountKey=tlRAtEUmclKrQPupGAnwlo6GyivJyVLI2DzsAlsDxCYbGx1896Jhsr6MOHShABk+ukTMsLSnUclt+AStgk6vww==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_blob(filename: str, container: str, file):
    try:
        blob_client = blob_service_client.get_blob_client(container = container, blob = filename)
        # upload data
        block_list=[]
        chunk_size=1024*1024*4
        with file.file as f:
            while True:
                read_data = f.read(chunk_size)
                if not read_data:
                    break # done
                blk_id = str(uuid.uuid4())
                blob_client.stage_block(block_id=blk_id,data=read_data) 
                block_list.append(BlobBlock(block_id=blk_id))
        blob_client.commit_block_list(block_list)
        message = "File uploaded successfully."
        return response_json(message)
    except BaseException as e:
        message = "ERROR File not processed."
        return response_json(message , status = 500)
            



    #try:
        #blob_client = blob_service_client.get_blob_client(container = container, blob = filename)
        #blob_client.upload_blob(data, overwrite=True)
        #return response_json(message="success")
    #except Exception as e:
        #return response_json(message=e.message, status = 500)
