import functions_framework
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.cloud import dataplex_v1
from google.cloud import storage
from datetime import datetime
import google.auth
import requests
import jsons
import os
import re

PROJECT = os.getenv('PROJECT', 'vanti-data-gobernance-dev')
LOCATION = os.getenv('LOCATION', 'us-central1')
BUCKET_DESTINATION = os.getenv('BUCKET_DESTINATION', 'vanti-data-gobernance-prd-dataplex-backup')

URL = f'projects/{PROJECT}/locations/{LOCATION}'

service_account_info = jsons.load({
"type": "service_account",
"project_id": "vanti-data-gobernance-dev",
"private_key_id": "7269921152d1b284af0a3a8d7291c4ff0677c360",
"private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCm2D5P0nEW0VMc\nhZSK76HVlCxZAXN6vRko0rAhTI4VfbB3HbhgJDve+4DA2hjYURWy0diue/4+u9xN\na1Aet+O6Dqeq/bJ5hIJywZIjRJyNb0dPJgYP6EF5lqyj0p1k3mO/iyS/uomuoU98\n5jEElSpBC/A4/Hjl9ZlscWSoX9bki+ufBg/vLKm9ORw4Wusa0Whl990rKcHW69YO\nWT6HvImugWolFjHqDPujTVI4IcTtVambm4JBBkvIzeS8ptPhozDdQHnJxkML6fpz\nzQat1Tf9NHDmiSCQTT7TDFZ1vjPRgyGmdWJM+FIj3db39DGZYwCxnG2Vml0H0hca\nD+qhqeErAgMBAAECggEAAtfxawnZvlelEM8ZV/JmI6ONWbenVgYgBiWzUf0ToxEh\nKDBU+3/Sl2YEewTx4q15UpZEpy7bB3zLKQLY0DjEp9+8LXpBh9RTQ0X7LXXr1yCU\n42DUsCya5RD+Kz8LZuXcg3UlzSKAPeG8e1ou/OgsWq8ddZpJSIi1+dpVjjsSlug2\nfPYGh9BiX2GN7adP2pcgG2sOw6kqK4xKHOfY4pjvbLqYlLNDA2oly3aqGy6XTlhN\nDpV4MHyjhhJivTxbSvvjMCWuyqxWEQEIPwomvXlVvWGSev3hLKc1hnDUhaI42q3N\n8N2z8RxjbqQldboJ8sWBCpu4/xxOCmc2awzXG7yBiQKBgQDmdExZvziQ23waL5ij\nuVoo86Hmf5S1vPvNvd1elreUox3CYknlX8suTywGwlj+AxaIRkqCcutXUNhnkLGL\nuZdkGfj8+8tHUwjPywIyXH2NWKw6bFMBCjBbA0TizI9bInb4B6zFbgAtdY/tFXtC\nTAKy0v9AXvuKmRR5YKxutaGZ0wKBgQC5Vt4+uTX/2eyVoJ+AvZHG1AZj9bFUAfHk\nkN8wu7iq9q4wFy2yY+s4Ne+1aN2pgN4z1eCAvP49QQK8jhIQoCEZ56/9YPfSTLbc\nVYC1kF34r4NRGbnpT7SQg+WwV7YWhqJi5KFWO1/e0e0rX/h7F5Bm5xWr/1Pg0wUX\nDJDkcZBsSQKBgQDE8Wh6Xh9yNBAXtMtGR9WUH7khabBlq86pIfP3rOfQX6HECAlM\nu5PAzKo8UISK94qfBSsR1jHnGdEGmLISTZXiVwvg7zHmj0B9i+khrschL0FoYECD\nJ/jxHpcVF2n/oTF4f96Xjo0aTFimbPA8VQcNWaIHmeRvqqjDneleZ1xmPwKBgEIp\nS27yqN8riTQkwauwgHCM0bcvRt0pUJN6T+JSsOp+4tGSBKMQ3jATuP12cOKIeUnh\nyKHMVanCIlrzEGnU79wShBWcXvs4nXJsJ2UpIxKafPMfjulFpbyNCRp5RSwnZaKN\n4TYqPeAJ6nM4cDhowgip52ed3vB8A+4lczfJfnfZAoGAExt+pEbZ8kWQ8WyXLPzn\nHr2wGvZd8qZCDRTV2CFszuteL+Oo2/78VR1boFpD3rxlOkZJ4LjvAHd8wSSC2bYm\n3HNTfLW9Pn5SSIg6gvvzcrk2z7V9Elf9+WX/O4hfOK6zIx4zGZwly/ME/5rjkXEZ\nHGT7ZYvM5LhNvGyJ9ZnLzhk=\n-----END PRIVATE KEY-----\n",
"client_email": "118338383205-compute@developer.gserviceaccount.com",
"client_id": "100767084161817572684",
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://oauth2.googleapis.com/token",
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/118338383205-compute%40developer.gserviceaccount.com",
"universe_domain": "googleapis.com"
})
credentials = service_account.Credentials.from_service_account_info(service_account_info)

def load_client(api_key):
    try:
        service = build("dataplex", "v1", credentials=api_key)
        return service
    except Exception as e:
        print("Error loading client for API", e)
        return None

def execute_list_scan(service, url):
    try:
        response = service.projects().locations().dataScans().list(
            parent = url
        ).execute()
        #print("Response", response)
        return response
    except Exception as e:
        print("Execute error", e)

def execute_configuration_scan(service, url):
    try:
        response = service.projects().locations().dataScans().get(
            name = url,
            view="FULL"
        ).execute()
        #print("Response", response)
        return str(response)
    except Exception as e:
        print("Execute error", e)

def copy_blob(destination_bucket_name, destination_blob, data):
    try:
        storage_client = storage.Client()
        destination_bucket = storage_client.bucket(destination_bucket_name)
        blob = destination_bucket.blob(destination_blob)
        blob.upload_from_string(data)
        print(f"file name: {destination_blob} copiado a {destination_bucket_name} como: {blob.name}")
    except Exception as e:
        print('Copy blob error', e)

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def backup_data_scan(cloud_event):
    date = datetime.today()
    actual_date = str(date.date()).replace('-','_')
    name_folder = actual_date[:-3]

    data = cloud_event.data
    event_id = cloud_event["id"]
    event_type = cloud_event["type"]
    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    service = load_client(credentials)
    if service:
        list_scans = execute_list_scan(service, URL)        
        coincidencias = re.findall("'name': '(.*?)'", str(list_scans))
        for name in coincidencias:
            name_scan = name.split('/')[-1]
            url_1 = URL + '/dataScans/' + name_scan
            path_destination = '/dataqualityscans/' + f'{name_folder}/' + name_scan + '_' + actual_date + '.json'
            #print(name_scan)
            #URL.append('projects/{PROJECT}/locations/{LOCATION}'+ scan['name'])
            resp = execute_configuration_scan(service, url_1)
            #print(resp)
            copy_blob(BUCKET_DESTINATION, path_destination, resp)