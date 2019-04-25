import boto3
import pathlib
import os
    

# define the path, I am using current dir
currentDirectory = pathlib.Path('.')

# search for csv files 
currentPattern = "*.csv"

for currentFile in currentDirectory.glob(currentPattern):  
    print(currentFile)
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(str(currentFile), 'mayur-eu-bucket-1',  str(currentFile))
    os.remove(currentFile)


