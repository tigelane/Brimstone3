CREATE SCHEMA `brimstone` ;

USE brimstone;

CREATE TABLE pay_types (
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    type TEXT 
);

INSERT INTO pay_types (type) VALUES ("Hourly");
INSERT INTO pay_types (type) VALUES ("Daily");
INSERT INTO pay_types (type) VALUES ("Round");
INSERT INTO pay_types (type) VALUES ("Multiple");

CREATE TABLE status (
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    status TEXT 
);

INSERT INTO status (status) VALUES ("Open");
INSERT INTO status (status) VALUES ("Assigned");
INSERT INTO status (status) VALUES ("Working");
INSERT INTO status (status) VALUES ("Invoice Ready");
INSERT INTO status (status) VALUES ("Closed");

CREATE TABLE gadget_types (
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    type TEXT 
);

INSERT INTO gadget_types (type) VALUES ("Super Dump");
INSERT INTO gadget_types (type) VALUES ("End Dump");
INSERT INTO gadget_types (type) VALUES ("Side Dump");
INSERT INTO gadget_types (type) VALUES ("Transfer");
INSERT INTO gadget_types (type) VALUES ("Conestoga");
INSERT INTO gadget_types (type) VALUES ("4 Axle");
INSERT INTO gadget_types (type) VALUES ("High Track Dozer");
INSERT INTO gadget_types (type) VALUES ("Bobcat");
INSERT INTO gadget_types (type) VALUES ("Partking Lot");
INSERT INTO gadget_types (type) VALUES ("Low Boy");

CREATE TABLE people_at_companies (
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    company_id INTEGER, 
    person_id INTEGER
);

CREATE TABLE peoples_gadgets (
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    person_id INTEGER, 
    gadget_id INTEGER
);

CREATE TABLE gadgets (
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    type INTEGER, 
    weight_rating INTEGER,
    name TEXT,
    notes TEXT
);

CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    name TEXT, 
    manager INTEGER,
    contact_info INTEGER,
    notes TEXT
);

CREATE TABLE people (
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    title TEXT, 
    first_name TEXT,
    last_name TEXT, 
    pref_name TEXT,
    contact_pref TEXT, 
    contact_info INTEGER,
    years_driving INTEGER,
    notes TEXT
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    assigned_person INTEGER,
    hiring_company INTEGER,
    start_date DATE,
    end_date DATE,  
    pay_type INTEGER,
    estimated_pay INTEGER, 
    gadget_type INTEGER,
    location INTEGER, 
    status INTEGER,
    pay_units INTEGER,
    name TEXT,
    person_rating INTEGER,
    company_rating INTEGER,
    pay_rate INTEGER,
    notes TEXT
);

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
