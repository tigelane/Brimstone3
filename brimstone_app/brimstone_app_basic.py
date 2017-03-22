#!/usr/bin/python
from flask import Flask, jsonify, request
app = Flask(__name__)

app_name = 'steameo'


# This application will run on TCP port
app_port = 5000

@app.route('/')
@app.route('/index')
def index():
    html = '''
        <center>
        <BODY style="color:#00FC00" bgcolor=black><H3>You have connected to the test server, not the real one.</H3>
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


@app.route('/incomming', methods=['POST'])
def incomming():
    print ("Incomming message!")
    reply = {'status': 'None'}
    request.get_data()
    inbound_message = request.json
    print ("Message from: {0}".format(request.environ['REMOTE_ADDR']))
    print ("Message ID: {0}".format(inbound_message["data"]["id"]))

    return jsonify(reply)

if __name__ == '__main__':
    app.config.update(
        DEBUG = True)
    app.run(host='0.0.0.0', port=app_port)
