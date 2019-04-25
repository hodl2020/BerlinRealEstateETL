import psycopg2
import awsconfig as cfg

con=psycopg2.connect(dbname=cfg.redshift['db'],host=cfg.redshift['host'],port=cfg.redshift['port'],user=cfg.redshift['user'],password=cfg.redshift['pwd'])


cur = con.cursor()

#insert facts about property and advt listing in fact table
#agent id and address id will be updated later by picking up surrogate keys from respective tables 
cur.execute("delete from fact_property;")
cur.execute("insert into fact_property select realEstateId ,0 agentId ,0 addressId ,  livingSpace ,usableFloorSpace ,numberOfBathRooms ,numberOfBedRooms ,numberOfRooms ,guestToilet ,TotalRent ,TotalRentScope ,deposit ,heatingCosts ,heatingCostsIncluded ,parkingSpacePrice ,hasPicture ,publishDate ,creationDate  ,modificationDate  ,availability_status from stg_property_data;")
cur.execute("delete from stg_agent_dim;")
cur.execute("insert into stg_agent_dim select realEstateId ,dense_rank() over(order by agent_firstname,agent_lastname,agent_email,agent_phoneNumber,agent_company ) agentId ,agent_company  ,agent_lastname  ,agent_firstname  ,agent_email  ,agent_cellPhoneNumber ,agent_phoneNumber from stg_property_data;")
cur.execute("delete from stg_address_dim;")
cur.execute("insert into stg_address_dim select realEstateId ,dense_rank() over(order by address_city,address_street,address_houseNumber,address_postcode,address_quarter ) addressId ,address_city  ,address_street  ,address_houseNumber  ,address_quarter  ,address_postcode ,address_latitude,address_longitude from stg_property_data;")


con.commit()

# populating dim tables and updating corresponding keys
cur.execute("update fact_property set agentId = stg_agent_dim.agentId from stg_agent_dim where stg_agent_dim.realEstateId = fact_property.realEstateId ;")
cur.execute("update fact_property set addressId = stg_address_dim.addressId from stg_address_dim where stg_address_dim.realEstateId = fact_property.realEstateId ;")
cur.execute("delete from agent_dim;")
cur.execute("insert into agent_dim select distinct agentId ,agent_company  ,agent_lastname  ,agent_firstname  ,agent_email  ,agent_cellPhoneNumber ,agent_phoneNumber from stg_agent_dim ;")
cur.execute("delete from address_dim;")
cur.execute("insert into address_dim select distinct addressId ,address_city  ,address_street  ,address_houseNumber  ,address_quarter  ,address_postcode ,address_latitude,address_longitude from stg_address_dim;")

con.commit()

cur.close()
con.close()

