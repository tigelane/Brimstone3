#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

##  This applicaiotn will run a web server and show anyone that connects the IP address
##  that Flask thinks is conencting to it.  This is useful for docker containers that are using
##  NAT and it's not apparent what IP Address they might be running on.

@app.route("/", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

if __name__ == '__main__':
    app.config.update(
            DEBUG=True)

    app.run(host='0.0.0.0', port=80)
