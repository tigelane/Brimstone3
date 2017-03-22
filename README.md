# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Overview: Creating a web front end for some Common ACI Tasks
* Version: .9

### How do I get set up? ###

* Use the Dockerfile to build a docker container
* Execute the docker container:  docker run -dp 80:80 <name_of_container>
* If you want to run it directly on a server, then use the steps in the Dockerfile to to do (built on Ubuntu 14.04)
* Dependencies are many, read the Dockerfile if you need to know


###  Running Local  ###
* By default the container will only respond to requests from the computer it's running on. - Not implemented yet
* Changes need to be made to the wicat.py file to allow Flask to respond to other computers.  
* Anyone connecting to the server could have access to the APIC via this tool.  
* The docker container provides some security for these credentials.

###  Python Requirements  ###
acitoolkit (For APIC integration)
ipaddress (For IP verification and manipulation)
paramiko (For SSH components)
beaker (For session handling with multiple users.)

###  environment.py  ###  
# Directory to store log files (Relative path)
log_dir = 'static/logs/'

# Main Menu width
menu_width = str(530)

# Page Title
applicationTitle = "WICAT"

# Graphic to use above menu
header_graphic_file = 'wu.png'

# CSS style file
style_wu_file = 'wu.css'

# Bootstrap files
style_bootstrap_file = 'bootstrap.min.css'
style_dataTables_bootstrap_file = 'dataTables.bootstrap.css'

# Fabric info
fabric_names = {'https://10.0.0.1': 'Fabric1',
               'https://10.128.0.1': 'Fabric2'}
			   
# Session Timeout (Seconds in Integer or None to disable)
session_timeout = None