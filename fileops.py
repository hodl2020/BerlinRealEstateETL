import datetime
import pathlib
import logging
import os


#getting current directory path
currentdirectory = pathlib.Path('.')

#Returns the name of the latest (most recent) file 
def get_latest_file(searchpattern):
    # logging configuration
    logging.basicConfig(filename='fileops.log', level=logging.INFO,
                    format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')
    try:
        list_of_files = currentdirectory.glob(searchpattern)  # list of files matching searchpattern
        if not list_of_files:                # prefer using the negation
            return None                      
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    except ValueError:
            logging.error("Check if file is present at local")    


def remove(currentfile):
    os.remove(currentfile)
