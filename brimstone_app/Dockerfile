FROM ubuntu:latest

MAINTAINER Tige Phillips <tige@tigelane.com>
# This container runs the application layer of Brimstone 3
# Brimstone is a an application to manage truck drivers

# Port to access the Flask application on - change if needed.
EXPOSE 5000

RUN apt-get update
RUN apt-get -y upgrade

#################
# GIT and MYSQL #
#################
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git mysql-client

####################
# PYTHON and TOOLS #
####################
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python2.7 python-pip python-dev libmysqlclient-dev
RUN DEBIAN_FRONTEND=noninteractive pip install MySQL-python flask

############
# Development only tools
############
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install vim
RUN pip install requests

#################
# Install                   #
#################
CMD mkdir /usr/local/brimstone
ADD brimstone_app.py /usr/local/brimstone/

#################
# App Options 
#################
# Place bash users directly into /usr/local/brimstone
WORKDIR /usr/local/brimstone

# Port to access the Flask application on - change if needed.
EXPOSE 5000

# By default when this container runs, simply start the application
CMD /usr/local/brimstone/brimstone_app.py