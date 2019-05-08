import psycopg2
import awsconfig as cfg
import boto3
import sys
import logging


def rsload():
    # logging configuration
    logging.basicConfig(filename='rsload.log', level=logging.INFO,
                        format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')
    # connect to redshift using connection defined awsconfig file
    con = psycopg2.connect(dbname=cfg.redshift['db'], host=cfg.redshift['host'],
                           port=cfg.redshift['port'], user=cfg.redshift['user'], password=cfg.redshift['pwd'])
    # incoming files are kept in below bucket
    in_bucket = cfg.s3c['in_bucket']
    # archived files are kept in below bucket
    arch_bucket = cfg.s3c['arch_bucket']
    # S3 access
    aws_access_key_id = cfg.s3c['key']
    aws_secret_access_key = cfg.s3c['skey']
    # connect to S3
    cur = con.cursor()
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(in_bucket)   
    
    #taking filename from S3 bucket and file is reguraly loaded then archived in archival bucket.
    for file in my_bucket.objects.all():
        #print (file.key)
        filename = file.key

    logging.info('{indent} uploading file: {filename}'.format(indent=3*' ', filename=filename))
    schema = 'public'
    table = 'stg_property_data'
    file_path = 's3://' + str(in_bucket) + '/' + str(filename)

    try:
        cur.execute("truncate table stg_property_data;")
        # copy csv from S3 to redshift table
        sql = """copy {}.{} from '{}'\
                        credentials \
                        'aws_access_key_id={};aws_secret_access_key={}' \
                        DELIMITER ','   removequotes ;"""\
                .format(schema, table, file_path, aws_access_key_id, aws_secret_access_key)
        cur.execute(sql)
        con.commit()
        # close connection
        cur.close()
        con.close()
    except Exception:
        # close connection in case of error as well
        cur.close()
        con.close()
        logging.error("Exception while copying file from S3 to Redshift", exc_info=True)

    # Archival of processed file to archival bucket
    copy_source = {
        'Bucket': in_bucket,
        'Key': filename
    }
    s3.meta.client.copy(copy_source, arch_bucket, filename)
    # Delete from current directory after archiving
    s3.Object(in_bucket, filename).delete()

if __name__ == "__main__":
    rsload()
