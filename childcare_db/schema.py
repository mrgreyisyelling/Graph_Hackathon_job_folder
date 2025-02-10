# Schema definitions for different entity types

# Facility Schema (Based on Provided Columns)
FACILITY_SCHEMA = {
    "Date Extracted": "TEXT",
    "License Number": "TEXT",
    "License Issue Date": "TEXT",
    "License Expiry Date": "TEXT",
    "License Type": "TEXT",
    "Facility Name": "TEXT",
    "Facility Address": "TEXT",
    "City": "TEXT",
    "State": "TEXT",
    "Zip Code": "INTEGER",
    "Phone Number": "TEXT",
    "Facility Type": "TEXT",
    "Operational Schedule": "TEXT",
    "Accepts Subsidies": "TEXT",
    "Hours of Operation (Sunday)": "TEXT",
    "Hours of Operation (Monday)": "TEXT",
    "Hours of Operation (Tuesday)": "TEXT",
    "Hours of Operation (Wednesday)": "TEXT",
    "Hours of Operation (Thursday)": "TEXT",
    "Hours of Operation (Friday)": "TEXT",
    "Hours of Operation (Saturday)": "TEXT",
    "School District Affiliation": "TEXT",
    "Alternative Address": "TEXT",
    "Facility Zip (Alt)": "INTEGER",
    "Alternative Contact Number": "TEXT",
    "Date Originally Licensed": "TEXT",
    "Facility Status": "TEXT"
}


# Location Schema (Based on Provided Columns)
LOCATION_SCHEMA = {
    "Facility Address": "TEXT",
    "City": "TEXT",
    "State": "TEXT",
    "Zip Code": "INTEGER",
    "Facility Zip (Alt)": "INTEGER",
    "Alternative Address": "TEXT"
}


# Owner Schema (Based on Provided Columns)
OWNER_SCHEMA = {
    "Facility Name": "TEXT",
    "License Number": "TEXT",
    "License Type": "TEXT",
    "Alternative Contact Number": "TEXT"
}

LICENSE_SCHEMA = {
    "License Number": "TEXT",
    "License Type": "TEXT",
    "License Issue Date": "TEXT",
    "License Expiry Date": "TEXT",
    "Facility Name": "TEXT",
    "Date Originally Licensed": "TEXT"
}

SCHOOL_DISTRICT_SCHEMA = {
    "Facility Name": "TEXT",
    "School District Affiliation": "TEXT"
}


# Dictionary to easily reference schemas
ENTITY_SCHEMAS = {
    "Facility": FACILITY_SCHEMA,
    "Location": LOCATION_SCHEMA,
    "Owner": OWNER_SCHEMA,
    "License": LICENSE_SCHEMA,
    "School District": SCHOOL_DISTRICT_SCHEMA
}
