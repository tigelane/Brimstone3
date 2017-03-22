#!/usr/bin/python
from flask import Flask, jsonify, request
app = Flask(__name__)

import MySQLdb, sys, os, json, requests
from datetime import datetime

app_name = 'brimstone'
app_version = "1.0"

db = None
db_name = app_name
#db_pass = 'mysql'
db_pass = 'H2xE6h6Bo9cgsnkiUhW076Qf'
db_addr = os.getenv('SQL_SERVER_IPADDR', 'localhost')

all_sql_query = 'SELECT jobs.id, people.first_name, companies.name, start_date, end_date, pay_types.type, estimated_pay, gadget_types.type, contact_info.city, status.status, pay_units, jobs.name, person_rating, company_rating, pay_rate, jobs.notes FROM jobs JOIN gadget_types ON jobs.gadget_type = gadget_types.id JOIN pay_types ON jobs.pay_type = pay_types.id JOIN status ON jobs.status = status.id JOIN companies ON jobs.hiring_company = companies.id JOIN contact_info ON jobs.location = contact_info.id JOIN people ON jobs.assigned_person = people.id;'
open_sql_query = 'SELECT jobs.id, people.first_name, companies.name, start_date, end_date, pay_types.type, estimated_pay, gadget_types.type, contact_info.city, status.status, pay_units, jobs.name, person_rating, company_rating, pay_rate, jobs.notes FROM jobs JOIN gadget_types ON jobs.gadget_type = gadget_types.id JOIN pay_types ON jobs.pay_type = pay_types.id JOIN status ON jobs.status = status.id JOIN companies ON jobs.hiring_company = companies.id JOIN contact_info ON jobs.location = contact_info.id JOIN people ON jobs.assigned_person = people.id WHERE status.status = "Open";'
edit_job_sql_query = 'SELECT jobs.id, people.first_name, companies.name, start_date, end_date, pay_types.type, estimated_pay, gadget_types.type, contact_info.city, status.status, pay_units, jobs.name, person_rating, company_rating, pay_rate, jobs.notes FROM jobs JOIN gadget_types ON jobs.gadget_type = gadget_types.id JOIN pay_types ON jobs.pay_type = pay_types.id JOIN status ON jobs.status = status.id JOIN companies ON jobs.hiring_company = companies.id JOIN contact_info ON jobs.location = contact_info.id JOIN people ON jobs.assigned_person = people.id WHERE jobs.id = '

# This application will run on the following TCP port
app_port = 5000

print "Attached to DB Server at: {0}".format(db_addr)

@app.route('/')
@app.route('/index')
def index():
    html = '''
        <center>
        <BODY style="color:#00FC00" bgcolor=black><H3>You have connected to the {0} application server</H3>
        '''.format(app_name)
    html += '''
        <p>
        Current date and time for this server: 
        '''
    html += datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html += '''
        <H3>(in a breathy voice while waving a hand infront of your face)<br>Go Back. This is not the web page you are looking for.</H3>
        <p>
        </BODY></HTML>
        '''
    return html

@app.route('/show_jobs/<jobs>/')
def show_jobs(jobs):

    if jobs == 'all':
        sql_query = all_sql_query
    else:
        sql_query = open_sql_query

    ''' Get all of the records and return them as a list of dictonarys'''
    myList = []
    
    try:
        open_db()
        cursor = db.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        for row in data:
            myList.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],row[10], row[11], row[12], row[13], row[14], row[15]])

        close_db()
        reply = {'status': 'OK', 'results': myList}
    except:
        reply = {'status': 'FAIL', 'results': "The Application server is OK, but is unable to show records from database {0}!".format(db_name)}
    
    return jsonify(reply)

@app.route('/remove_db')
def remove_db():
    ''' Remove the database '''
    sql_query = "DROP DATABASE {0};".format(db_name)

    try:
        open_mysql()
        open_db()
        cursor = db.cursor()
        cursor.execute(sql_query)

        close_db()
        reply = {'status': 'OK', 'results': "Database {0} has been removed!".format(db_name)}
    except:
        reply = {'status': 'FAIL', 'results': "Unable to remove database {0}!".format(db_name)}

    return jsonify(reply)

def open_mysql():
    global db
    ''' Opens a connection to MySQL at the given IP Address '''
	
    try:
        # Open database connection
        db = MySQLdb.connect(db_addr,"root",db_pass)
        return True
    except:
        return False

def create_db():
	''' Create a new database '''

	try:
		sql_query = "CREATE DATABASE IF NOT EXISTS {0};".format(db_name)
		cursor = db.cursor()
		cursor.execute(sql_query)
	except:
		return False

	return True

def open_db():
    global db
    ''' Opens the database at the given IP Address '''
    	
    try:
        # Open database connection
        db = MySQLdb.connect(db_addr, "root", db_pass, db_name)
    except:
        return False

    return True

def close_db():
    global db
    # disconnect from server
    db.close()


@app.route('/edit_job/<job_id>/')
def edit_job(job_id):

    sql_query = "{0}{1};".format(edit_job_sql_query, job_id)
    ''' Get all of the records and return them as a list of dictonarys'''
    myList = []
    
    try:
        open_db()
        cursor = db.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        for row in data:
            myList.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],row[10], row[11], row[12], row[13], row[14], row[15]])

        close_db()
        reply = {'status': 'OK', 'results': myList}
    except:
        reply = {'status': 'FAIL', 'results': "The Application server is OK, but is unable to show records from database {0}!".format(db_name)}
    
    return jsonify(reply)


@app.route('/add_row')
def add_row(text, date, name):
	# Use the right database
	sql_query = "INSERT INTO entry (id, entry, entry_date, name) VALUES (NULL, '{0}', '{1}', '{2}');".format(text, date, name)
	open_db()
	cursor = db.cursor()	
	cursor.execute(sql_query)
	db.commit()

	close_db()
	return

@app.route('/add_entry', methods=['POST'])
def add_entry():
    try:
        name = request.args.get("name")
        entry = request.args.get("entry")
        now = datetime.now()
        date = "{0}-{1}-{2}".format(now.year, now.month, now.day)
        add_row(entry, date, name)
    except:
        return jsonify({'status': 'FAIL', 'results': "Not able to post to the database!"})

    return jsonify({'status': 'OK', 'results': "Blog Entry Posted!"})

def for_me(message):
    if (message.split(' ', 1)[0] == "/{0}".format(app_name)):
        return True
    return False


    # Also, GET /messages requires that you specify a special ?mentionedPeople=me query parameter.

    # GET /messages?mentionedPeople=me&roomId=SOME_INTERESTING_ROOM
    # Authorization: Bearer THE_BOTS_ACCESS_TOKEN

@app.route('/incomming', methods=['POST'])
def incomming():
    # print ("Incomming message!")
    now = datetime.now()
    date = "{0}-{1}-{2}".format(now.year, now.month, now.day)
    reply = {'status': 'None'}
    request.get_data()
    inbound_message = request.json
    # print (request.data)
    # print (request.form)
    #print (request.json)
    # print ("Message from: {0}".format(request.environ['REMOTE_ADDR']))
    messageurl = "https://api.ciscospark.com/v1/messages/{}".format(inbound_message["data"]["id"])

    headers = {
        'authorization': sparkUser,
        'content-type': "application/json",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", messageurl, headers=headers)
    messagedata = json.loads(response.text)
    print messagedata
    try:
        message = "You betya!"
        # print("Spark room message is: {0}".format(messagedata["text"]))
        # if for_me(messagedata["text"]):
        # add_row(messagedata["text"], date, 'Steameo')
        # post_message_to_room(post_room_id, message)
        reply = {'status': 'OK'}
    except ValueError:
        print ("We have an error:  {0}".format(response.content))
        reply = {'status': 'Error'}

    return jsonify(reply)



if __name__ == '__main__':
	app.config.update(
		DEBUG = True)

	app.run(host='0.0.0.0', port=app_port)