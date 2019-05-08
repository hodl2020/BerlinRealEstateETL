import boto3
import pathlib
import logging
import fileops

    

def uploads3():
        # configure logging
        logging.basicConfig(filename = 's3upload.log',level=logging.INFO,
                    format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s',
                    )
        # search for csv files 
        searchpattern = "*.csv"
        try:
            # get latest filename
            currentfile = fileops.get_latest_file(searchpattern)
            #upload to s3
            s3 = boto3.resource('s3')
            s3.meta.client.upload_file(str(currentfile), 'incoming-eu-bucket-2',  str(currentfile))
            logging.info('{indent} uploading file: {filename}'.format(indent=3*' ', filename=currentfile))
            # remove current file from local (you can archive if needed)
            fileops.remove(currentfile)
        except Exception:
            logging.error("Exception while uploading file to S3", exc_info=True)
            

if __name__ == "__main__":
    uploads3()
