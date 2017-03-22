USE brimstone;

INSERT INTO people_at_companies (company_id, person_id) VALUES (1,1);
INSERT INTO people_at_companies (company_id, person_id) VALUES (1,2);
INSERT INTO people_at_companies (company_id, person_id) VALUES (2,3);
INSERT INTO people_at_companies (company_id, person_id) VALUES (3,4);
INSERT INTO people_at_companies (company_id, person_id) VALUES (3,5);

INSERT INTO peoples_gadgets (person_id, gadget_id) VALUES (1,1);
INSERT INTO peoples_gadgets (person_id, gadget_id) VALUES (2,1);
INSERT INTO peoples_gadgets (person_id, gadget_id) VALUES (3,2);
INSERT INTO peoples_gadgets (person_id, gadget_id) VALUES (4,3);
INSERT INTO peoples_gadgets (person_id, gadget_id) VALUES (5,3);

INSERT INTO gadgets (type, weight_rating, name) VALUES (1,80000,"The Dog");
INSERT INTO gadgets (type, weight_rating, name) VALUES (2,75000,"The hulk");
INSERT INTO gadgets (type, weight_rating, name) VALUES (3,50000,"Slider");
INSERT INTO gadgets (type, weight_rating, name) VALUES (4,45000,"Viper");
INSERT INTO gadgets (type, weight_rating, name) VALUES (5,55000,"Merlin");

INSERT INTO companies (name, manager, contact_info, notes) VALUES ("Bobs Consturuction",1,1,"They Suck");
INSERT INTO companies (name, manager, contact_info, notes) VALUES ("Builders Warehouse",2,2,"Pay fast");
INSERT INTO companies (name, manager, contact_info, notes) VALUES ("Smittys",3,3,"Wow");

INSERT INTO people (title, first_name, last_name, pref_name, contact_pref, contact_info, notes) VALUES ("driver","Bob","Smith","Bobby","call office",1,"Be sure ot check the day before.");
INSERT INTO people (title, first_name, last_name, pref_name, contact_pref, contact_info, notes) VALUES ("owner","Tim","Martin","Tim","email",2,"Can't backup to save his life");
INSERT INTO people (title, first_name, last_name, pref_name, contact_pref, contact_info, notes) VALUES ("manager","Steven","Marxs","Steve","text message",3,"Always a little loose with the hours");
INSERT INTO people (title, first_name, last_name, pref_name, contact_pref, contact_info, notes) VALUES ("driver","Dale","Barber","Dave","call cell",4,"Great end dumper");
INSERT INTO people (title, first_name, last_name, pref_name, contact_pref, contact_info, notes) VALUES ("driver","Susan","Palin","Suzy","text message",5,"Wno't need any supervision");

INSERT INTO jobs (assigned_person, hiring_company, pay_type, gadget_type, location, status, pay_units, name, pay_rate, notes) VALUES (1,1,1,1,1,1,2, "Hell Road move",15,"Be sure to to get overloaded, scales");
INSERT INTO jobs (assigned_person, hiring_company, pay_type, gadget_type, location, status, pay_units, name, pay_rate, notes) VALUES (2,2,2,1,1,1,1, "sand lot",22,"be there by 7am first day for briefing");
INSERT INTO jobs (assigned_person, hiring_company, pay_type, gadget_type, location, status, pay_units, name, pay_rate, notes) VALUES (3,1,3,2,3,1,2, "I5 Night Paving",320,"Arrive 5pm");
INSERT INTO jobs (assigned_person, hiring_company, pay_type, gadget_type, location, status, pay_units, name, pay_rate, notes) VALUES (4,3,3,3,2,1,1, "spider river crossing",21,"channel 18 for conners");
INSERT INTO jobs (assigned_person, hiring_company, pay_type, gadget_type, location, status, pay_units, name, pay_rate, notes) VALUES (5,1,4,4,4,2,1, "house cutout",18,"call bob 503-555-1212 at 9am for gate code");

INSERT INTO contact_info (email, web_site, mobile_phone, nic_name, city) VALUES ("bob@someconstu.com","www.someconstru.com","503-555-1212","Main office", "Beaverton");
INSERT INTO contact_info (email, web_site, mobile_phone, nic_name, city) VALUES ("mark@someotherco.com","www.builders.com","545-234-4579","Office", "Portland");
INSERT INTO contact_info (email, web_site, mobile_phone, nic_name, city) VALUES ("rickjames@buildingscheap.com","buildingscheap.com","234.987.4569","Headquarters", "Gresham");
INSERT INTO contact_info (email, web_site, mobile_phone, nic_name, city) VALUES ("fatguy@googe.com","www.fatguytrucking.com","545-234-4579","Office", "Oregon City");
INSERT INTO contact_info (email, web_site, mobile_phone, nic_name, city) VALUES ("ldysman@mac.com","ladysloveme.com","234.987.4569","Headquarters", "Brightwood");

