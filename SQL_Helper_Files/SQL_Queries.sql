SELECT jobs.id, assigned_person, hiring_company, start_date, end_date, pay_type, estimated_pay, gadget_types.type, location, status, pay_units, name, person_rating, company_rating, notes 
FROM jobs 
JOIN gadget_types ON jobs.gadget_type = gadget_types.id;

SELECT jobs.id, people.first_name, companies.name, start_date, end_date, pay_types.type, estimated_pay, gadget_types.type, contact_info.city, status.status, pay_units, jobs.name, person_rating, company_rating, pay_rate, jobs.notes 
FROM jobs 
JOIN gadget_types ON jobs.gadget_type = gadget_types.id
JOIN pay_types ON jobs.pay_type = pay_types.id
JOIN status ON jobs.status = status.id
JOIN companies ON jobs.hiring_company = companies.id
JOIN contact_info ON jobs.location = contact_info.id
JOIN people ON jobs.assigned_person = people.id;



SELECT jobs.id, people.first_name, companies.name, start_date, end_date, pay_types.type, estimated_pay, gadget_types.type, contact_info.city, status.status, pay_units, jobs.name, person_rating, company_rating, pay_rate, jobs.notes FROM jobs JOIN gadget_types ON jobs.gadget_type = gadget_types.id JOIN pay_types ON jobs.pay_type = pay_types.id JOIN status ON jobs.status = status.id JOIN companies ON jobs.hiring_company = companies.id JOIN contact_info ON jobs.location = contact_info.id JOIN people ON jobs.assigned_person = people.id WHERE status.status = "Open";