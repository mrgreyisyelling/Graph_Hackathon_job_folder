#!/bin/bash

# Navigate to the correct directory
cd ~/Documents/Programming/Graph_Hackathon_job_folder/childcare_db

# Export Locations
sqlite3 childcare.db -csv -header "SELECT location_id, city, state, zip_code FROM locations;" > locations.csv

# Export Facilities
sqlite3 childcare.db -csv -header "SELECT facility_id, facility_name, phone_number, facility_type, accepts_subsidies FROM facilities;" > facilities.csv

# Export Owners
sqlite3 childcare.db -csv -header "SELECT owner_id, license_number, alternative_contact_number FROM owners;" > owners.csv

# Export Licenses
sqlite3 childcare.db -csv -header "SELECT license_id, license_number, license_type, license_issue_date, license_expiry_date FROM licenses;" > licenses.csv

# Export School Districts
sqlite3 childcare.db -csv -header "SELECT district_id, district_name FROM school_districts;" > school_districts.csv

# Verify files were created
ls -lah *.csv


sudo mv locations.csv /var/lib/neo4j/import/
sudo mv facilities.csv /var/lib/neo4j/import/
sudo mv owners.csv /var/lib/neo4j/import/
sudo mv licenses.csv /var/lib/neo4j/import/
sudo mv school_districts.csv /var/lib/neo4j/import/
