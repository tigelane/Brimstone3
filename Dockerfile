FROM ubuntu:latest

MAINTAINER Tige Phillips <tige@tigelane.com>
# This container runs Brimstone
# A web application for manageing truck drivers

RUN apt-get update ;\
        apt-get -y upgrade

####################
# PYTHON and TOOLS #
####################
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python2.7 python-pip python-dev libmysqlclient-dev
RUN DEBIAN_FRONTEND=noninteractive pip install flask requests

############
# Development only tools, could be removed later
############
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install vim

#################
# App install 
#################
RUN mkdir /usr/local/brimstone
ADD brimstone_web.py /usr/local/brimstone
ADD static /usr/local/brimstone/static/
ADD templates /usr/local/brimstone/templates/

#################
# App Options 
#################
# Place bash users directly into /usr/local/brimstone
WORKDIR /usr/local/brimstone

# Port to access the Flask application on - change if needed.
EXPOSE 80

# By default when this container runs, simply start the application
CMD RUN mkdir /usr/local/brimstone/brimstone_web.py
