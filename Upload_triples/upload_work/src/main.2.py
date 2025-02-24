
import sqlite3
import hashlib
import json
from datetime import datetime

### ✅ Step 1: Utility Functions

def generate_id(value, prefix):
    """Generate a unique ID for a given value."""
    return hashlib.md5(f"{prefix}:{value}".encode()).hexdigest()


### ✅ Step 2: Schema Definitions
SCHEMA_DEFINITIONS = {
    "Facility": {
        "schema_id": generate_id("Facility", "Schema"),
        "attributes": ["facility_name", "facility_status", "facility_type", "accepts_subsidies"],
        "relationships": {
            "LOCATED_AT": "Location",
            "OWNED_BY": "Owner",
            "LICENSED_UNDER": "License",
            "FOLLOWS_SCHEDULE": "Schedule",
            "AFFILIATED_WITH": "SchoolDistrict"
        }
    },
    "Location": {
        "schema_id": generate_id("Location", "Schema"),
        "attributes": [],
        "relationships": {
            "LOCATED_IN": "City",
            "IN_STATE": "State",
            "HAS_ZIP": "ZipCode",
            "HAS_ADDRESS": "Address",
            "USES_TIMEZONE": "TimeZone"
        }
    },
    "City": {
        "schema_id": generate_id("City", "Schema"),
        "attributes": ["name"],
        "relationships": {
            "IN_STATE": "State"
        }
    },
    "State": {
        "schema_id": generate_id("State", "Schema"),
        "attributes": ["name"],
        "relationships": {}
    },
    "ZipCode": {
        "schema_id": generate_id("ZipCode", "Schema"),
        "attributes": ["zip_code"],
        "relationships": {
            "IN_CITY": "City",
            "IN_STATE": "State"
        }
    },
    "Address": {
        "schema_id": generate_id("Address", "Schema"),
        "attributes": ["full_address"],
        "relationships": {
            "BELONGS_TO": "Location"
        }
    },
    "TimeZone": {
        "schema_id": generate_id("TimeZone", "Schema"),
        "attributes": ["name"],
        "relationships": {
            "USED_BY": "Location"
        }
    },
    "Owner": {
        "schema_id": generate_id("Owner", "Schema"),
        "attributes": ["alternative_contact_number"],
        "relationships": {
            "HAS_PHONE": "PhoneNumber",
            "OWNS_FACILITY": "Facility",
            "HOLDS_LICENSE": "License"
        }
    },
    "PhoneNumber": {
        "schema_id": generate_id("PhoneNumber", "Schema"),
        "attributes": ["number"],
        "relationships": {
            "USED_BY": ["Owner", "Facility", "Business"]
        }
    },
    "License": {
        "schema_id": generate_id("License", "Schema"),
        "attributes": ["license_number", "date_originally_licensed"],
        "relationships": {
            "GRANTED_TO": "Facility",
            "HAS_TYPE": "LicenseType",
            "ISSUED_ON": "Date",
            "EXPIRES_ON": "Date"
        }
    },
    "LicenseType": {
        "schema_id": generate_id("LicenseType", "Schema"),
        "attributes": ["name"],
        "relationships": {
            "USED_IN": "License"
        }
    },
    "Date": {
        "schema_id": generate_id("Date", "Schema"),
        "attributes": ["date_value"],
        "relationships": {
            "RELATED_TO": ["License", "BirthYear"]
        }
    },
    "Schedule": {
        "schema_id": generate_id("Schedule", "Schema"),
        "attributes": [],
        "relationships": {
            "HAS_OPERATION_HOURS": "ScheduleEntry"
        }
    },
    "ScheduleEntry": {
        "schema_id": generate_id("ScheduleEntry", "Schema"),
        "attributes": [],
        "relationships": {
            "HAS_DAY": "DayOfWeek",
            "OPENS_AT": "Time",
            "CLOSES_AT": "Time",
            "STATUS": "Status"
        }
    },
    "DayOfWeek": {
        "schema_id": generate_id("DayOfWeek", "Schema"),
        "attributes": ["day"],
        "relationships": {
            "PART_OF": "ScheduleEntry"
        }
    },
    "Time": {
        "schema_id": generate_id("Time", "Schema"),
        "attributes": ["time_value"],
        "relationships": {
            "USED_IN": "ScheduleEntry"
        }
    },
    "SchoolDistrict": {
        "schema_id": generate_id("SchoolDistrict", "Schema"),
        "attributes": ["district_name"],
        "relationships": {
            "OVERSEES": "Facility"
        }
    },
    "BirthYear": {
        "schema_id": generate_id("BirthYear", "Schema"),
        "attributes": ["year"],
        "relationships": {
            "BORN_IN": "Person"
        }
    },
    "AgeGroup": {
        "schema_id": generate_id("AgeGroup", "Schema"),
        "attributes": ["label"],
        "relationships": {
            "BELONGS_TO": "Person"
        }
    },
    "Status": {
        "schema_id": generate_id("Status", "Schema"),
        "attributes": ["status"],
        "relationships": {
            "USED_IN": "ScheduleEntry"
        }
    }
}



def parse_row_data(row, column_indexes):
    """Extracts row data into a structured object."""
    return {
        "facility_name": row[column_indexes["Facility Name"]],
        "facility_status": row[column_indexes["Facility Status"]],
        "facility_type": row[column_indexes["Facility Type"]],
        "accepts_subsidies": row[column_indexes["Accepts Subsidies"]],
        "city": row[column_indexes["City"]],
        "state": row[column_indexes["State"]],
        "zip_code": row[column_indexes["Zip Code"]],
        "alternative_zip": row[column_indexes["Facility Zip (Alt)"]],
        "address": row[column_indexes["Facility Address"]],
        "alternative_address": row[column_indexes["Alternative Address"]],
        "license_number": row[column_indexes["License Number"]],
        "license_type": row[column_indexes["License Type"]],
        "date_originally_licensed": row[column_indexes["Date Originally Licensed"]],
        "license_issue_date": row[column_indexes["License Issue Date"]],
        "license_expiry_date": row[column_indexes["License Expiry Date"]],
        "school_district": row[column_indexes["School District Affiliation"]],
        "alternative_contact_number": row[column_indexes["Alternative Contact Number"]]
    }


data = parse_row_data(row, column_indexes)


    import hashlib

# Global ID dictionary
ID_INDEX = {
    "Entity": {},        # Stores entity type -> ID
    "Attribute": {},     # Stores attribute name -> ID
    "Relationship": {}   # Stores relationship type -> ID
}

def get_or_create_id(value, category):
    """
    Retrieves an existing ID if the value exists in ID_INDEX,
    otherwise generates a new one and stores it.
    
    Args:
        value (str): The name of the entity, attribute, or relationship.
        category (str): One of ["Entity", "Attribute", "Relationship"].
    
    Returns:
        str: The unique ID for the given value.
    """

    # Ensure the category exists in the dictionary
    if category not in ID_INDEX:
        raise ValueError(f"Invalid category: {category}")

    # Check if ID already exists
    if value in ID_INDEX[category]:
        return ID_INDEX[category][value]

    # Generate a new unique ID
    unique_id = hashlib.md5(f"{category}:{value}".encode()).hexdigest()

    # Store the new ID
    ID_INDEX[category][value] = unique_id

    return unique_id


def get_or_create_attributes(entity_type, data):
    """Retrieve or create attribute IDs and return them as a dictionary."""
    schema = SCHEMA_DEFINITIONS[entity_type]
    attributes_with_ids = {}

    for attr in schema["attributes"]:
        if attr in data:
            attr_id = get_or_create_id(attr, "Attribute")
            attributes_with_ids[attr_id] = {
                "name": attr,
                "value": data[attr]
            }

    return attributes_with_ids

    
def get_or_create_relationship(from_id, to_id, relationship_type):
    """Retrieve or create a relationship and return its ID."""
    if not from_id or not to_id:  # Ensure valid IDs before creating relationships
        return None

    relationship_id = get_or_create_id(f"{from_id}->{to_id}", "Relationship")
    return {
        "relationship_id": relationship_id,
        "from": from_id,
        "to": to_id,
        "type": relationship_type
    }

    
ENTITY_DEFINITIONS = {
        "Facility": lambda data: f"{data['facility_name']}|{data['license_number']}|{data['address']}",
        "Location": lambda data: f"{data['address']}|{data['city']}|{data['state']}|{data['zip_code']}",
        "Owner": lambda data: f"{data['facility_name']}_person",
        "License": lambda data: data["license_number"],
        "SchoolDistrict": lambda data: data["school_district"],
        "Schedule": lambda data: f"{data['operational_schedule']}|{data['Hours of Operation (Sunday)']}|{data['Hours of Operation (Monday)']}|{data['Hours of Operation (Tuesday)']}|{data['Hours of Operation (Wednesday)']}|{data['Hours of Operation (Thursday)']}|{data['Hours of Operation (Friday)']}|{data['Hours of Operation (Saturday)']}"
    }
    
def get_or_create_entity(entity_type, data):
        """
        Retrieve or create an entity ID using standardized definitions.

        Args:
            entity_type (str): The entity type (e.g., "Facility", "Location").
            data (dict): The row data used for unique identification.

        Returns:
            str: The unique ID of the entity.
        """
        if entity_type not in ENTITY_DEFINITIONS:
            raise ValueError(f"Entity type '{entity_type}' is not defined.")

        # Generate the unique key based on the entity definition
        unique_key = ENTITY_DEFINITIONS[entity_type](data)

        # Get or create the entity ID
        entity_id = get_or_create_id(unique_key, "Entity")

        return entity_id

def process_facility(data):
        """Processes a single row of data to create a Facility entity, its relationships, and related entities."""
    
        # Retrieve or create Facility entity
        facility_id = get_or_create_entity("Facility", data)
    
        # Retrieve or create attributes
        attributes = get_or_create_attributes("Facility", data)
    
        # Retrieve or create related entities using standardized definitions
        location_id = get_or_create_entity("Location", data)
        owner_id = get_or_create_entity("Owner", data)
        license_id = get_or_create_entity("License", data)
        school_district_id = get_or_create_entity("SchoolDistrict", data)
        schedule_id = get_or_create_entity("Schedule", data)
    
        # Retrieve or create relationships
        relationships = [
            get_or_create_relationship(facility_id, location_id, "LOCATED_AT"),
            get_or_create_relationship(facility_id, owner_id, "OWNED_BY"),
            get_or_create_relationship(facility_id, license_id, "LICENSED_UNDER"),
            get_or_create_relationship(facility_id, school_district_id, "AFFILIATED_WITH"),
            get_or_create_relationship(facility_id, schedule_id, "FOLLOWS_SCHEDULE")
        ]
    
        # Construct Facility entity
        facility_entity = {
            "entity_id": facility_id,
            "type": "Facility",
            "schema_id": get_or_create_id("Facility", "Entity"),
            "attributes": attributes,
            "relationships": relationships
        }
    
        return facility_entity

def process_location(data):
    """Processes a Location entity, defining its attributes and relationships."""
    location_id = get_or_create_entity("Location", data)
    attributes = get_or_create_attributes("Location", data)
    
    # Related Entities
    city_id = get_or_create_entity("City", data)
    state_id = get_or_create_entity("State", data)
    zipcode_id = get_or_create_entity("ZipCode", data)
    address_id = get_or_create_entity("Address", data)
    timezone_id = get_or_create_entity("TimeZone", data)

    # Relationships
    relationships = [
        get_or_create_relationship(location_id, city_id, "LOCATED_IN"),
        get_or_create_relationship(location_id, state_id, "IN_STATE"),
        get_or_create_relationship(location_id, zipcode_id, "HAS_ZIP"),
        get_or_create_relationship(location_id, address_id, "HAS_ADDRESS"),
        get_or_create_relationship(location_id, timezone_id, "USES_TIMEZONE")
    ]

    return {"entity_id": location_id, "type": "Location", "attributes": attributes, "relationships": relationships}


def process_owner(data):
    """Processes an Owner entity."""
    owner_id = get_or_create_entity("Owner", data)
    attributes = get_or_create_attributes("Owner", data)

    phone_id = get_or_create_entity("PhoneNumber", data)
    facility_id = get_or_create_entity("Facility", data)
    license_id = get_or_create_entity("License", data)

    relationships = [
        get_or_create_relationship(owner_id, phone_id, "HAS_PHONE"),
        get_or_create_relationship(owner_id, facility_id, "OWNS_FACILITY"),
        get_or_create_relationship(owner_id, license_id, "HOLDS_LICENSE")
    ]

    return {"entity_id": owner_id, "type": "Owner", "attributes": attributes, "relationships": relationships}


def process_license(data):
    """Processes a License entity."""
    license_id = get_or_create_entity("License", data)
    attributes = get_or_create_attributes("License", data)

    facility_id = get_or_create_entity("Facility", data)
    license_type_id = get_or_create_entity("LicenseType", data)
    issue_date_id = get_or_create_entity("Date", {"date_value": data["license_issue_date"]})
    expiry_date_id = get_or_create_entity("Date", {"date_value": data["license_expiry_date"]})

    relationships = [
        get_or_create_relationship(license_id, facility_id, "GRANTED_TO"),
        get_or_create_relationship(license_id, license_type_id, "HAS_TYPE"),
        get_or_create_relationship(license_id, issue_date_id, "ISSUED_ON"),
        get_or_create_relationship(license_id, expiry_date_id, "EXPIRES_ON")
    ]

    return {"entity_id": license_id, "type": "License", "attributes": attributes, "relationships": relationships}


def process_school_district(data):
    """Processes a School District entity."""
    district_id = get_or_create_entity("SchoolDistrict", data)
    attributes = get_or_create_attributes("SchoolDistrict", data)

    facility_id = get_or_create_entity("Facility", data)

    relationships = [
        get_or_create_relationship(district_id, facility_id, "OVERSEES")
    ]

    return {"entity_id": district_id, "type": "SchoolDistrict", "attributes": attributes, "relationships": relationships}


def process_schedule(data):
    """Processes a Schedule entity."""
    schedule_id = get_or_create_entity("Schedule", data)
    attributes = get_or_create_attributes("Schedule", data)

    facility_id = get_or_create_entity("Facility", data)
    schedule_entries = [get_or_create_entity("ScheduleEntry", {"day": day, "time": data[f"Hours of Operation ({day})"]})
                        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]]

    relationships = [get_or_create_relationship(schedule_id, entry, "HAS_OPERATION_HOURS") for entry in schedule_entries]

    return {"entity_id": schedule_id, "type": "Schedule", "attributes": attributes, "relationships": relationships}


def process_schedule_entry(data, day):
    """Processes a single ScheduleEntry entity for a given day."""
    schedule_entry_id = get_or_create_entity("ScheduleEntry", {"day": day, "time": data[f"Hours of Operation ({day})"]})
    attributes = get_or_create_attributes("ScheduleEntry", {"day": day, "time": data[f"Hours of Operation ({day})"]})

    day_of_week_id = get_or_create_entity("DayOfWeek", {"day": day})
    open_time_id = get_or_create_entity("Time", {"time_value": data[f"Hours of Operation ({day})"].split('-')[0]})
    close_time_id = get_or_create_entity("Time", {"time_value": data[f"Hours of Operation ({day})"].split('-')[-1]})

    relationships = [
        get_or_create_relationship(schedule_entry_id, day_of_week_id, "HAS_DAY"),
        get_or_create_relationship(schedule_entry_id, open_time_id, "OPENS_AT"),
        get_or_create_relationship(schedule_entry_id, close_time_id, "CLOSES_AT")
    ]

    return {"entity_id": schedule_entry_id, "type": "ScheduleEntry", "attributes": attributes, "relationships": relationships}


def process_day_of_week(data):
    """Processes a DayOfWeek entity."""
    day_id = get_or_create_entity("DayOfWeek", data)
    attributes = get_or_create_attributes("DayOfWeek", data)

    return {"entity_id": day_id, "type": "DayOfWeek", "attributes": attributes, "relationships": []}


def process_time(data):
    """Processes a Time entity."""
    time_id = get_or_create_entity("Time", data)
    attributes = get_or_create_attributes("Time", data)

    return {"entity_id": time_id, "type": "Time", "attributes": attributes, "relationships": []}


def process_status(data):
    """Processes a Status entity."""
    status_id = get_or_create_entity("Status", data)
    attributes = get_or_create_attributes("Status", data)

    return {"entity_id": status_id, "type": "Status", "attributes": attributes, "relationships": []}
