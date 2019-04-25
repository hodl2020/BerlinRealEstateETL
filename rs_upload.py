import psycopg2
import awsconfig as cfg
import boto3
import sys

con=psycopg2.connect(dbname=cfg.redshift['db'],host=cfg.redshift['host'],port=cfg.redshift['port'],user=cfg.redshift['user'],password=cfg.redshift['pwd'])

cur = con.cursor()

s3 = boto3.resource('s3')
my_bucket = s3.Bucket('mayur-eu-bucket-1')

i=0

#taking filename from S3 bucket 
for file in my_bucket.objects.all():
    #print (file.key)
    i += 1
    filename = file.key

if i==0:
        #print ('Exiting since there is no file')
        sys.exit(0)        

schema = 'public'
table = 'stg_property_data'
file_path = 's3://mayur-eu-bucket-1/'+ str(filename)
aws_access_key_id = cfg.s3['key']
aws_secret_access_key = cfg.s3['skey']

cur.execute("truncate table stg_property_data;")

#copy csv from S3 to redshift table
sql="""copy {}.{} from '{}'\
        credentials \
        'aws_access_key_id={};aws_secret_access_key={}' \
        DELIMITER ','   removequotes ;"""\
        .format(schema, table, file_path, aws_access_key_id, aws_secret_access_key)


cur.execute(sql)
con.commit()
cur.close()
con.close()

#Archival of processed file
copy_source = {
        'Bucket': 'mayur-eu-bucket-1',
        'Key': filename
    }
s3.meta.client.copy(copy_source, 'arch-eu-bucket-2',filename)
s3.Object('mayur-eu-bucket-1',filename).delete()
