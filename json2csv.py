import pandas as pd
from pandas.io.json import json_normalize
import calendar
import time
import logging
import fileops


def jparse():
    # search for json files
    searchpattern = '*.json'
    # logging configuration
    logging.basicConfig(filename='json2csv.log', level=logging.INFO,
                    format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')
    try:
        #get latest filename 
        currentfile = fileops.get_latest_file(searchpattern)
        # Read Json file and then flatten it
        jdata = pd.read_json(currentfile, lines=True)
        df = json_normalize(jdata['data'])
        # Fetch required columns into dataframe
        parsed_df = df[['realEstate_id', 'realEstate_livingSpace', 'realEstate_usableFloorSpace', 'realEstate_numberOfBathRooms', 'realEstate_numberOfBedRooms', 'realEstate_numberOfRooms', 'realEstate_guestToilet', 'realEstate_calculatedTotalRent', 'realEstate_calculatedTotalRentScope', 'realEstate_deposit', 'realEstate_heatingCosts', 'realEstate_heatingCostsInServiceCharge', 'realEstate_parkingSpacePrice', 'realEstate_titlePicture_titlePicture', 'publishDate', 'creation',
                        'modification', 'realEstate_state', 'realEstate_address_geoHierarchy_city_name', 'realEstate_address_street', 'realEstate_address_houseNumber', 'realEstate_address_quarter', 'realEstate_address_postcode', 'realEstate_address_wgs84Coordinate_latitude', 'realEstate_address_wgs84Coordinate_longitude', 'contactDetails_company', 'contactDetails_lastname', 'contactDetails_firstname', 'contactDetails_email', 'contactDetails_cellPhoneNumber', 'contactDetails_phoneNumber']]
        # timestamp taken to append to csv name
        ts = calendar.timegm(time.gmtime())
        # save it as csv
        parsed_df.to_csv('rsdata_'+str(ts)+'.csv',
                         header=0, index=False)
        logging.info('{indent} parsing file: {filename}'.format(indent=3*' ', filename=currentfile))
        # remove json so that there is no unnecessary reload
        #fileops.remove(currentfile)
    except Exception:
        logging.error("Exception parsing json", exc_info=True)
        


if __name__ == "__main__":
    jparse()
