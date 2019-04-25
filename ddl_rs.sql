create table stg_property_data
(
realEstateId int,
livingSpace real,
usableFloorSpace real,
numberOfBathRooms real,
numberOfBedRooms real,
numberOfRooms real,
guestToilet varchar(50),
TotalRent real,
TotalRentScope varchar (50),
deposit varchar (100),
heatingCosts real,
heatingCostsIncluded varchar (30),
parkingSpacePrice real,
hasPicture varchar (10),
publishDate varchar (50),
creationDate varchar (50) ,
modificationDate varchar (50) ,
availability_status varchar (30),
address_city varchar (30),
address_street varchar (50),
address_houseNumber  varchar (30),
address_quarter varchar(50),
address_postcode real,
address_latitude NUMERIC (10,8),
address_longitude NUMERIC (10,8),
agent_company  varchar (100),
agent_lastname  varchar (100),
agent_firstname  varchar (50),
agent_email  varchar (50),
agent_cellPhoneNumber varchar (100),
agent_phoneNumber varchar (100))
;

create table stg_agent_dim
(
realEstateId int,
agentId int,
agent_company  varchar (100),
agent_lastname  varchar (100),
agent_firstname  varchar (50),
agent_email  varchar (50),
agent_cellPhoneNumber varchar (100),
agent_phoneNumber varchar (100)
)
;


create table stg_address_dim
(
realEstateId int,
addressId int,
address_city varchar (30),
address_street varchar (50),
address_houseNumber  varchar (30),
address_quarter varchar(50),
address_postcode real,
address_latitude NUMERIC (10,8),
address_longitude NUMERIC (10,8)
)
;


create table fact_property
(
realEstateId int,
agentId int,
addressId int,  
livingSpace real,
usableFloorSpace real,
numberOfBathRooms real,
numberOfBedRooms real,
numberOfRooms real,
guestToilet varchar(50),
TotalRent real,
TotalRentScope varchar (50),
deposit varchar (100),
heatingCosts real,
heatingCostsIncluded varchar (30),
parkingSpacePrice real,
hasPicture varchar (10),
publishDate varchar (50),
creationDate varchar (50) ,
modificationDate varchar (50) ,
availability_status varchar (30))
;


create table address_dim
(
addressId int,
address_city varchar (30),
address_street varchar (50),
address_houseNumber  varchar (30),
address_quarter varchar(50),
address_postcode real,
address_latitude NUMERIC (10,8),
address_longitude NUMERIC (10,8)
)
;

create table agent_dim
(
agentId int,
agent_company  varchar (100),
agent_lastname  varchar (100),
agent_firstname  varchar (50),
agent_email  varchar (50),
agent_cellPhoneNumber varchar (100),
agent_phoneNumber varchar (100)
)
;