# Backup Scans de Calidad de Dataplex

##Implementación de arquitectura para realizar copias de seguridad de Dataplex a Cloud Storage.


Este documento describe el proceso para implementar una Cloud Function en Google Cloud Platform (GCP), este proceso consiste en disparar una cloud function mediante Cloud Scheduler. La función ejecuta un script de python que realiza una copia de seguridad de los análisis de calidad de datos y de perfilamiento de Dataplex en un bucket de Cloud Storage.

!["Arquitectura implementada"](/src/architecture.drawio.png)


## Implementación

Para llevar a cabo el proceso descrito anteriormente se deben implementar los siguientes servicios:

Cuenta de servicio: Permite otorgar acceso a recursos de GCP a aplicaciones y servidores.  
Cloud Function: Implementa la lógica para realizar la copia de seguridad de los análisis de Dataplex.  
Cloud Scheduler: Programa la ejecución de una Cloud Function cada día a las 23:00 horas.  
Cloud Storage (Bucket): Almacena las copias de seguridad de los análisis de calidad de datos de dataplex.  
Dataplex API: Proporciona acceso a los datos de Dataplex para realizar la copia de seguridad.  

#### Parte 1: Creación cuenta de servicio
#### Parte 2: Creación cloud function
#### Parte 3: Creación cloud schedule
#### Parte 4: Creación (Bucket) cloud storage




## Parte 1: Creación cuenta de servicio (sa-backupdqsc-dplex-gob-dq) y asignación de permiso para lectura de datos de Datascan.


```bash

gcloud config set project vanti-data-gobernance-prd


gcloud iam service-accounts create sa-backupdqsc-dplex-gob-dq \
--description="Cuenta de servicio para backup data scans dataplex" \
--display-name="sa-backupdqsc-dplex-gob-dq"

gcloud projects add-iam-policy-binding vanti-data-gobernance-prd \
--member='serviceAccount:sa-backupdqsc-dplex-gob-dq@vanti-data-gobernance-prd.iam.gserviceaccount.com' \
--role='roles/dataplex.dataScanDataViewer'

gcloud projects add-iam-policy-binding vanti-data-gobernance-prd \
--member='serviceAccount:sa-backupdqsc-dplex-gob-dq@vanti-data-gobernance-prd.iam.gserviceaccount.com' \
--role='roles/iam.serviceAccountUser'


```

## Parte 2: Creación cloud function (cf-dataplex-dataquality-scans-backup)

dirigase a la URL: https://console.cloud.google.com/functions de su proyecto

-Haga clic en create funtion  
-Ponga el nombre a la cloud function "cf-dataplex-dataquality-scans-backup"  
-Escoja la región "us-central1"  
-Escoja el trigger "HTTPS" y "Require authentication"  
-En la sección "Runtime, build, connections and security settings" despliegue y en "Runtime service account" ponga:  
 la cuenta de servicio que se creó en el paso 1 "sa-backupdqsc-dplex-gob-dq@vanti-data-gobernance-prd.iam.gserviceaccount.com"  
-En la sección "Runtime environment variables" agregue las siguientes variables de entorno:  

PROJECT            = vanti-data-gobernance-prd  
LOCATION_1         = us-central1  
LOCATION_2         = us-east1  
BUCKET_DESTINATION = vanti-data-gobernance-prd-dataplex-backup  

Haga clic en next  

-En la casilla Runtime escoja "python 3.10"  
-En la casilla entry point coloque "backup_data_scans"  
-Copie y pegue el código que está en main.py de este repositorio en main.py del area de trabajo de la cloud function  
-Copie y pegue el código que está en requirements.txt de este repositorio en requirements.txt del area de trabajo de la cloud function  
-Haga clic en deploy.  

-Luego de haber creado la cloud function, dar clic en la cloud fucntion creada y en la casilla permisos darle permiso a la cuenta  "sa-backupdqsc-dplex-gob-dq@vanti-data-gobernance-prd.iam.gserviceaccount.com"  


## Parte 3: Creación cloud schedule

dirigase a la URL: https://console.cloud.google.com/cloudscheduler de su proyecto  

Haga clic en create job

Coloque el nombre del cloud schedule "cs-dataplex-dataquality-execute-backup"  
Escoja la región "us-central1"  
Coloque una descripción para el cloud schedule  
coloque la siguiente configuración de frecuencia de ocurrencia "0 23 * * *" para que ocurra cada día a las 23:00 horas  
En la casilla Timezone escoja Colombia

En la sección "Configure the execution" escoja la opción HTTP

Haga clic en crear.

Luego de haber creado el schedule, dar clic en el schedule creado y en la casilla permisos darle permiso a la cuenta  "sa-backupdqsc-dplex-gob-dq@vanti-data-gobernance-prd.iam.gserviceaccount.com"



## Parte 4: Creación (Bucket) cloud storage

dirigase a la URL: https://console.cloud.google.com/storage de su proyecto  

Hacer clic en create  

Poner el nombre de bucket "vanti-data-gobernance-prd-dataplex-backup"  
En la sección tipo de localización escojer "Region"  
En la sección clase de almacenamiento escojer "Standard"  
En la sección cómo controlar el acceso a los objetos escojer "Aplicar la prevención de acceso público en este segmento" y "uniforme"  
En la sección cómo proteger los datos del objeto escojer "Política de eliminación temporal (para recuperación de datos) y 7 días de duración"  
Activar el control de versiones así:  
"Política de eliminación temporal (para recuperación de datos)" 10 días  
"Política de eliminación temporal (para recuperación de datos)" 10 días  

Haga clic en crear 

Luego de haber creado el Bucket, dar clic en el Bucket creado y en la casilla permisos darle permiso a la cuenta  "sa-backupdqsc-dplex-gob-dq@vanti-data-gobernance-prd.iam.gserviceaccount.com"  


