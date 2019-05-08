import psycopg2
import awsconfig as cfg
import logging


def rselt():
    try:
        # logging configuration
        logging.basicConfig(filename='elt.log', level=logging.INFO,format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')
        #connect to redshift db
        con=psycopg2.connect(dbname=cfg.redshift['db'],host=cfg.redshift['host'],port=cfg.redshift['port'],user=cfg.redshift['user'],password=cfg.redshift['pwd'])
        cur = con.cursor()
        #insert facts about property and advt listing in fact table
        #agent id and address id will be updated later by picking up surrogate keys from respective tables. Since there are no natural keys and tables are reloaded every refresh on Redshift pretty easily hence I am using dense_rank for surrogate key. Safer way is to use sha-256 hashing.  
        cur.execute("truncate table fact_property;")
        cur.execute("insert into fact_property select realEstateId ,0 agentId ,0 addressId ,  livingSpace ,usableFloorSpace ,numberOfBathRooms ,numberOfBedRooms ,numberOfRooms ,guestToilet ,TotalRent ,TotalRentScope ,deposit ,heatingCosts ,heatingCostsIncluded ,parkingSpacePrice ,hasPicture ,publishDate ,creationDate  ,modificationDate  ,availability_status from stg_property_data;")
        cur.execute("truncate table stg_agent_dim;")
        cur.execute("insert into stg_agent_dim select realEstateId ,dense_rank() over(order by agent_firstname,agent_lastname,agent_email,agent_phoneNumber,agent_company ) agentId ,agent_company  ,agent_lastname  ,agent_firstname  ,agent_email  ,agent_cellPhoneNumber ,agent_phoneNumber from stg_property_data;")
        cur.execute("truncate table stg_address_dim;")
        cur.execute("insert into stg_address_dim select realEstateId ,dense_rank() over(order by address_city,address_street,address_houseNumber,address_postcode,address_quarter ) addressId ,address_city  ,address_street  ,address_houseNumber  ,address_quarter  ,address_postcode ,address_latitude,address_longitude from stg_property_data;")
        con.commit()
        # populating dim tables and updating corresponding keys
        cur.execute("update fact_property set agentId = stg_agent_dim.agentId from stg_agent_dim where stg_agent_dim.realEstateId = fact_property.realEstateId ;")
        cur.execute("update fact_property set addressId = stg_address_dim.addressId from stg_address_dim where stg_address_dim.realEstateId = fact_property.realEstateId ;")
        cur.execute("truncate table agent_dim;")
        cur.execute("insert into agent_dim select distinct agentId ,agent_company  ,agent_lastname  ,agent_firstname  ,agent_email  ,agent_cellPhoneNumber ,agent_phoneNumber from stg_agent_dim ;")
        cur.execute("truncate table address_dim;")
        cur.execute("insert into address_dim select distinct addressId ,address_city  ,address_street  ,address_houseNumber  ,address_quarter  ,address_postcode ,address_latitude,address_longitude from stg_address_dim;")
        con.commit()
        cur.close()
        con.close()
    except Exception:
        # close connection in case of error as well
        cur.close()
        con.close()
        logging.error("Exception while copying file from S3 to Redshift", exc_info=True)    
    
if __name__ == "__main__":
    rselt()
