ELT Pipeline Example [Real Estate Data]
==================

## Table of Contents
- [Installation](#Installation)
- [Airflow and Python Setup](#Airflow)
- [Airflow UI](#Airflow_UI)
- [Python_Scripts_Description](#Python_Scripts_Description)
- [Create Dag](#Dag)

## Installation 
- __Python:__ Python 3.6 or higher
- __S3 bucket:__ create incoming and archival buckets on AWS S3 (incoming-eu-bucket-2 and arch-eu-bucket-2)
- __EC2:__ spin up an ec2 instance with ubuntu where we can install airflow
- __Redshift:__ Create redshift db instance
- __DDL:__ create staging and target tables needed for star schema as present in ddl_rs.sql 
- __AWS Config:__ 1) pip3 install awscli 2) aws configure (provide access key and secret key) 3) awsconfig.py (import while connecting to redshift/S3).Add IP address to security group of aws. In production it will be AWS IAM policy.

## Airflow and Python packages Setup
Do this:
- $ sudo apt-get update
- $ sudo apt install python3-pip
- $ pip3 install boto3==1.3.0
- $ pip3 install pandas
- $ sudo apt-get install libpq-dev
- $ pip3 install psycopg2
- $ pip3 install awscli
- $ export AIRFLOW_HOME=/home/ubuntu/airflow
- $ sudo pip3 install apache-airflow
- $ airflow initdb
- $ airflow scheduler -D
- $ airflow webserver -D

## Airflow_UI 
- open port 8080: 
http://ec2-18-184-1-86.eu-central-1.compute.amazonaws.com:8080/admin/


## Python_Scripts_Description

- json2csv.py
- json to real estate data csv (timestamped) and removes json file after csv creation (we can move it to archive location if needed)
- s3upload.py
- s3upload.py uploads current csv file to s3 and removes it from local. Files are overwritten on S3 if already existing.
- rs_upload.py
- S3 to redshift, copy csv to redshift in staging table and moves csv file to archival bucket
- rs_elt.py
- Populates dim and fact tables from stage table on redshift.



## Create Dag


