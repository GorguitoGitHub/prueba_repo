# Backup Scans Calidad


## Set project

```bash
gcloud config set project vanti-data-gobernance-prd
```


## Service Account

```bash
gcloud gcloud iam service-accounts create sa-backupdqsc-dplex-gob-dq --description "Cuenta de servicio para backup data scans dataplex"

gcloud projects add-iam-policy-binding vanti-data-gobernance-prd \
--member sa-backupdqsc-dplex-gob-dq@vanti-data-gobernance-dev.iam.gserviceaccount.com \
--role roles/run.invoker \
--condition="resource.zone == 'us-central1'"

gcloud projects add-iam-policy-binding vanti-data-gobernance-prd \
--member sa-backupdqsc-dplex-gob-dq@vanti-data-gobernance-dev.iam.gserviceaccount.com \
--role roles/cloudfunctions.invoker \
--condition="resource.zone == 'us-central1'"