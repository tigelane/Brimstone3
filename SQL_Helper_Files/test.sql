CREATE SCHEMA `brimstone` ;

USE brimstone;

CREATE TABLE contact_info (
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    email TEXT,
    web_site TEXT,
    mobile_phone TEXT,
    office_phone TEXT,
    street_address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    country TEXT,
    facebook TEXT,
    twitter TEXT,
    nic_name TEXT,
    notes TEXT
);
