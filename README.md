# BerlinRealEstateETL
Datapipeline creation for loading json input data to AWS Redshift


## pre·requisite
Python 3.6 or higher installed

## Installations

pip install pandas

## s3 bucket name (one for incoming csv and second for archival of loaded data)
#mayur-eu-bucket-1 
#arch-eu-bucket-2


## aws cli installation
pip install awscli

# aws configure 
Also used awsconfig.py
I am configuring access keys for test purpose, in production it will be AWS IAM policy.


## add IP address to security group of aws

## below libraries for file handling on S3 and SQL execution on redshift
pip install boto3
pip install psycopg2

## create tables on redshift db present in ddl_rs.sql  

## step1 json to real estate data csv (timestamped) and removes json file after csv creation (we can move it to archive location if needed)
python3 json2csv.py

## step2 s3upload.py uploads current csv file to s3 and removes it from local. Files are overwritten on S3 if already existing.
python3 s3upload.py 

## step3 S3 to redshift, copy csv to redshift in staging table and moves csv file to archival bucket
python3 rs_upload.py

## step4 transformation part of ELT, populates dim and fact tables from stage tables
python3 rs_elt.py

## step5 setting up airflow dag



