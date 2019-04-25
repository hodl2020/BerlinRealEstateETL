import pandas as pd
import re
import json
from pandas.io.json import json_normalize
import calendar
import time
#import sys
import os
import pathlib
    

# define the path, I am using current dir
currentDirectory = pathlib.Path('.')

# search for json files 
currentPattern = "*immobilienscout24*.json"

for currentFile in currentDirectory.glob(currentPattern):  
    #print(currentFile)
    jdata = pd.read_json(currentFile, lines=True)
    df = json_normalize(jdata['data'])
    parsed_df = df[['realEstate_id','realEstate_livingSpace','realEstate_usableFloorSpace','realEstate_numberOfBathRooms','realEstate_numberOfBedRooms','realEstate_numberOfRooms','realEstate_guestToilet','realEstate_calculatedTotalRent','realEstate_calculatedTotalRentScope','realEstate_deposit','realEstate_heatingCosts','realEstate_heatingCostsInServiceCharge','realEstate_parkingSpacePrice','realEstate_titlePicture_titlePicture','publishDate','creation','modification','realEstate_state','realEstate_address_geoHierarchy_city_name','realEstate_address_street','realEstate_address_houseNumber','realEstate_address_quarter','realEstate_address_postcode','realEstate_address_wgs84Coordinate_latitude','realEstate_address_wgs84Coordinate_longitude','contactDetails_company','contactDetails_lastname','contactDetails_firstname','contactDetails_email','contactDetails_cellPhoneNumber','contactDetails_phoneNumber']] 
    ts = calendar.timegm(time.gmtime())
    #print(ts)
    parsed_df.to_csv('rsdata_'+str(ts)+'.csv',header=0,index=False)
    os.remove(currentFile)



#path = 'D:\Python\pyproject\immobilienscout24_berlin_20190113.json'
#path = 'D:\Python\pyproject\small.json'
#print(sys.getsizeof(df))
#print(parsed_df.nunique())
#print(parsed_df)

