#!/usr/bin/env python

from flask import Flask, request, render_template, url_for, redirect, session

from datetime import datetime
import sys, requests, re, random, os
import json, time

applicationTitle = "Brimstone"
header_graphic_files = ["truck_pic_1.png", "truck_pic_2.png", "truck_pic_3.png", "truck_pic_4.png", "truck_pic_5.png", "truck_pic_6.png", "truck_pic_7.png"]
style_file = "brimstone.css"
app_addr = os.getenv('APP_SERVER_IPADDR', 'localhost')
app_port = 5000

app = Flask(__name__)

@app.route('/')
def default():

    url = 'http://{0}:{1}/show_jobs/open/'.format(app_addr, app_port)

    title = "Open Jobs"

    data = open_url(url)
    if data['result'] == 0:
        return data['data']

    else:
        records = data['data']
        html = table_header()
        html += render_template('show_open_jobs.html', title=title, records=records)
        html += table_footer()

    return html

def base_menu():
    """
    Draw initial screen and menu items.
    :return: html pages as rendered html
    """    
    html = render_template('menu_template.html', header_graphic=get_header_graphic(), app_title=applicationTitle, style_guide=get_style_link())
    return html

def table_footer():
    """
    Should be inlcuded on all table based screens
    :return: html pages as rendered html
    """
    return  render_template('table_footer.html')

def render_error_screen(error):
    """
    Takes the error as a string, returns full html page to display
    :param error: Error code
    :return: html pages as rendered html
    """
    # Render HTML
    html = base_menu()
    html += render_template('error.html',
                            error=error)
    return html

def get_header_graphic():
    """
    Should be included on all screens, pics a rangome graphic for the top of the screen
    :return: url_for to the graphic for the header. 
    """
    header_graphic_file = header_graphic_files[random.randint(0, len(header_graphic_files)-1)]
    return url_for('static', filename=header_graphic_file)

def table_header():
    """
    Should be included on all table based screens - includes the base menu
    :return: html pages as rendered html
    """
    html = base_menu()
    html += render_template('table_header.html')
    return html

def get_style_link():
    return url_for('static', filename=style_file)

def open_url(url):
    try: 
        result = requests.get(url)
    except:
        error = "Application Server Failure: Not able to communicate with Application Server at {0} ".format(app_addr)
        return {'result':0, 'data':render_error_screen(error)}

    if (result.status_code == 200):
        decoded_json = json.loads(result.text)
        if decoded_json['status']== 'FAIL':
            error = "Database Failure: Response from Application Server: " + decoded_json['results']
            return {'result':0, 'data':render_error_screen(error)}

        if len(decoded_json['results']) == 0:
            error = "Response from Application Server: No records found."
            return {'result':0, 'data':render_error_screen(error)}

    # Need to check if there was another error.  Will have to look at the othe web page to find what it's doing.
    # if 0 == 1:
    #     pass
    # else:   
    #     error = "Application Server Failure: We did not receive a proper response from the application server.  Status Code != 200: " + result.text
    #     return render_error_screen(error)

    return {'result':1, 'data':decoded_json['results']}

@app.route('/login', methods=['GET'])
def login_get():

    html = base_menu()
    html += render_template('login.html')

    return html

@app.route('/login', methods=['POST'])
def login_post():
    session['username'] = str(request.form['username'])
    session['password'] = str(request.form['password'])
    return redirect('/server_info', code=303)

@app.route('/server_info')
def server_info():
    """
    Renders HTML for Server Info Page
    :return:
    """
    # Render HTML
    html = base_menu()
    html += render_template('server_info.html',
                            title='Server Info',
                            version=sys.version_info,
                            datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return html

@app.route('/new_job', methods=['GET'])
def new_job():
    """
    Render entry page for a new job
    :return: html pages as rendered html
    """

    html = base_menu()
    html += render_template('enter_new_job.html')
    return html

@app.route('/add_new_job', methods=['POST'])
def add_new_job():
    """
    Gather data from form post and post information to database
    :return: html pages as rendered html
    """
    if request.form["button"] == "cancel":
        return redirect('/server_info', code=303)

    formValues = {}
    formValues["hco"] = request.form['hco']
    formValues["ttype"] = request.form['ttype']
    formValues["loc"] = request.form['loc']

    #  Look for missing items and show an error screen if needed
    for k, v in formValues.iteritems():
        if v == "":
            return render_error_screen("You must specify all of the '*' values.")

    # Add the rest to values that are optional
    formValues["sdate"] = request.form['sdate']
    formValues["epay"] = request.form['epay']
    
    print formValues
    return redirect('/server_info', code=303)

@app.route('/edit_job/<job_id>/')
def edit_job(job_id):
    
    url = 'http://{0}:{1}/edit_job/{2}/'.format(app_addr, app_port, job_id)

    title = "Edit Job"

    data = open_url(url)
    if data['result'] == 0:
        return data['data']

    else:
        records = data['data']
        html = table_header()
        html += render_template('show_open_jobs.html', title=title, records=records)
        html += table_footer()

    return html

@app.route('/new_gadget', methods=['GET'])
def new_gadget():
    """
    Render entry page for a new job
    :return: html pages as rendered html
    """

    html = base_menu()
    html += render_template('enter_new_gadget.html')
    return html

@app.route('/add_new_gadget', methods=['POST'])
def add_new_gadget():
    """
    Gather data from form post and post information to database
    :return: html pages as rendered html
    """
    time_start = time.time()
    if request.form["button"] == "cancel":
        return redirect('/', code=303)

    formValues = {}
    formValues["type"] = request.form['type']

    #  Look for missing items and show an error screen if needed
    for k, v in formValues.iteritems():
        if v == "":
            return render_error_screen("You must specify all of the '*' values.")

    print (request.form)

    # Add the rest to values that are optional
    # formValues["contact"] = request.form['contact']
    # formValues["email"] = request.form['email']
    # formValues["notes"] = request.form['notes']
    # formValues[""] = request.form['']
    

    message = "Gadget Added: {}".format(formValues["type"])

    html = table_header()
    html += render_template('add_record.html', thecolor="green", header="Success", message=message)
    html += table_footer()

    print 'Time to complete posting of new gadget: ', time.time() - time_start
    return html

@app.route('/new_person', methods=['GET'])
def new_person():
    """
    Render entry page for a new job
    :return: html pages as rendered html
    """

    html = base_menu()
    html += render_template('enter_new_person.html')
    return html

@app.route('/add_new_person', methods=['POST'])
def add_new_person():
    """
    Gather data from form post and post information to database
    :return: html pages as rendered html
    """

    if request.form["button"] == "cancel":
        return redirect('/server_info', code=303)

    formValues = {}
    formValues["fname"] = request.form['fname']
    formValues["lname"] = request.form['lname']
    formValues["phone"] = request.form['phone']

    #  Look for missing items and show an error screen if needed
    for k, v in formValues.iteritems():
        if v == "":
            return render_error_screen("You must specify all of the '*' values.")

    print (request.form)

    # Add the rest to values that are optional
    formValues["contact"] = request.form['contact']
    formValues["email"] = request.form['email']
    formValues["notes"] = request.form['notes']
    # formValues[""] = request.form['']
    
    print (formValues)
    return redirect('/server_info', code=303)


@app.route('/show_jobs/<jobs>/')
def show_jobs(jobs):

    url = 'http://{0}:{1}/show_jobs/{2}/'.format(app_addr, app_port, jobs)
    
    if jobs == 'all':
        title = "All Jobs"
    else:
        title = "Open Jobs"

    data = open_url(url)
    if data['result'] == 0:
        return data['data']

    else:
        records = data['data']
        html = table_header()
        html += render_template('show_jobs.html', title=title, records=records)
        html += table_footer()

    return html

@app.route('/search_host')
def search_host():
    """
    Render Search for an Endpoint Page page
    :return: html pages as rendered html
    """

    # Render HTML
    tenant_list = []
    tenants = get_user_tenants()
    for tenant in tenants:
        tenant_list.append(tenant.name)

    html = base_menu()
    html += render_template('search_host.html', tenants=tenant_list)
    return html

@app.route('/search_host', methods=['POST'])
def search_host_post():
    """
    Gather data from form post and render search results
    :return: html pages as rendered html
    """
    time_start = time.time()
    aciSession = login_to_apic(session)
    if type(aciSession) is list:
        return aciSession[2]
    try:
        tenant_name = request.form['tenant_name']
    except:
        return render_error_screen("You must specify a tenant that you would like to search in")
    text = request.form['text']


    records = []

    tenants = get_user_tenants()
    for tenant in tenants:
        if tenant_name.upper() in tenant.name.upper() or tenant_name == 'all':
            apps = aci.AppProfile.get(aciSession, tenant)
            for app in apps:
                epgs = aci.EPG.get(aciSession, app, tenant)
                for epg in epgs:
                    # endpoints = aci.Endpoint.get_all_by_epg(aciSession, tenant.name, app.name, epg.name, with_interface_attachments=False)
                    endpoints = c1.get_epg_info(aciSession, tenant.name, app.name, epg.name)
                    for ep in endpoints:
                        for match in [ep.ip.upper(), ep.mac.upper(), ep.encap.upper(), ep.if_name.upper(), tenant.name.upper(), app.name.upper(), epg.name.upper()]:
                            if text.upper() in match:
                                records.append((ep.mac, ep.ip, ep.if_name, ep.encap,
                                            tenant.name, app.name, epg.name))
                                break


    html = table_header()
    html += render_template('search_host_post.html', text=text, records=set(records))
    html += table_footer()
    print 'Time to complete: ', time.time() - time_start
    return html

@app.route('/search_contract')
def search_contract():
    """
    Render Contract Details search form.
    :return:
    """
    # Render HTML
    html = base_menu()
    html += render_template('search_contract.html')
    return html

@app.route('/search_contract', methods=['POST'])
def search_contract_post():
    """
    Gather data from form post and render search results
    :return:
    """
    aciSession = login_to_apic(session)
    if type(aciSession) is list:
        return aciSession[2]

    text = request.form['text']


    # Download all of the tenants, app profiles, and EPGs
    # and store the names as tuples in a list
    records = []
    CONTRACTS = c1.ContractMap()

    tenants = aci.Tenant.get_deep(aciSession)
    for tenant in tenants:
        for contract in tenant.get_children():
            if isinstance(contract, aci.Contract):
                if text.upper() in contract.name.upper():
                    CONTRACTS.names.append(contract.name)
                    CONTRACTS.filters[contract.name] = []
                    CONTRACTS.tenant[contract.name] = tenant.name
                    for subject in contract.get_children():
                        url = '/api/node/mo/uni/tn-%s/brc-%s/subj-%s.json?query-target=children' % (tenant.name, contract.name, subject.name)
                        resp = aciSession.get(url)
                        dns = json.loads(resp.text)['imdata']
                        for dn in dns:
                            filter_name = dn['vzRsSubjFiltAtt']['attributes']['tRn'][4:]


                            records.append((tenant.name, contract.name, filter_name))
                            url = '/api/node/mo/uni/tn-%s/flt-%s.json?query-target=children&target-subtree-class=vzEntry' % (tenant.name, filter_name)

                            resp = aciSession.get(url)
                            dns = json.loads(resp.text)['imdata']
                            for dn in dns:
                                dFromPort = dn['vzEntry']['attributes']['dFromPort']
                                dToPort = dn['vzEntry']['attributes']['dFromPort']
                                prot = dn['vzEntry']['attributes']['prot']
                                if dFromPort == dToPort:
                                    dlistPort = prot + ':' + dFromPort
                                else:
                                    dlistPort = prot + ':' + dFromPort + '-' + dToPort
                                CONTRACTS.filters[contract.name].append(filter_name + ' (' + dlistPort + ')')


    # Render HTML
    html = table_header()
    html += render_template('search_contract_post.html', CONTRACTS=CONTRACTS)
    html += table_footer()
    return html






if __name__ == '__main__':
    # app.secret_key = os.urandom(24)
    app.secret_key = "abcde12345"
    app.config.update(
            DEBUG=True)

    app.run(host='0.0.0.0', port=80)
