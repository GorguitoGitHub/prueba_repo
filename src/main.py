import functions_framework
from googleapiclient.discovery import build
from google.cloud import dataplex_v1
from google.cloud import storage
from datetime import datetime
import google.auth
import requests
import jsons
import pytz
import os
import re

print('---prende---')

PROJECT            = os.getenv('PROJECT', 'vanti-data-gobernance-prd')
LOCATION_1         = os.getenv('LOCATION_1', 'us-central1')
LOCATION_2         = os.getenv('LOCATION_2', 'us-east1')
BUCKET_DESTINATION = os.getenv('BUCKET_DESTINATION', 'vanti-data-gobernance-prd-dataplex-backup')

URL_BASE = f'projects/{PROJECT}/locations/'
LOCATIONS = [LOCATION_1, LOCATION_2]

def load_client():
    try:
        service = build("dataplex", "v1")
        return service
    except Exception as e:
        print("Error loading client for API", e)
        return None

def execute_list_scan(service, url):
    try:
        response = service.projects().locations().dataScans().list(
            parent = url,
            pageSize = "1000"
        ).execute()
        return str(response).encode('utf-8')
    except Exception as e:
        print("Execute error", e)

def execute_configuration_scan(service, url):
    try:
        response = service.projects().locations().dataScans().get(
            name = url,
            view="FULL"
        ).execute()
        return str(response).encode('utf-8')
    except Exception as e:
        print("Execute error", e)

def copy_blob(destination_bucket_name, destination_blob, data):
    try:
        storage_client = storage.Client()
        destination_bucket = storage_client.bucket(destination_bucket_name)
        blob = destination_bucket.blob(destination_blob)
        blob.upload_from_string(data, content_type="application/json")
        print(f"file name: {destination_blob} copiado a {destination_bucket_name} como: {blob.name}")
    except Exception as e:
        print('Copy blob error', e)

@functions_framework.http
def backup_data_scans(request):

    colombia_time_zone = pytz.timezone('America/Bogota')
    date_time = datetime.now(colombia_time_zone)
    actual_date = str(date_time.date()).replace('-','_')
    name_folder = actual_date[:-3]

    print(f'---INICIA--- {request} -- ENVIRONS: {os.environ}')
    
    service = load_client()
    if service:
        for location in LOCATIONS:
            URL = URL_BASE + location
            list_scans = execute_list_scan(service, URL)        
            coincidencias = re.findall("'name': '(.*?)'", str(list_scans))
            for name in coincidencias:
                name_scan = name.split('/')[-1]
                url_config = URL + '/dataScans/' + name_scan
                path_destination = 'dataqualityscans/' + f'{name_folder}/' + name_scan + '_' + actual_date + '.json'
                resp = execute_configuration_scan(service, url_config)
                copy_blob(BUCKET_DESTINATION, path_destination, resp)
    
    print('--- Final Function ---')

    return 'ok'