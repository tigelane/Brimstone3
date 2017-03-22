#!/usr/bin/env python

# list of packages that should be imported for this code to work
import re
import requests
from cobra.mit.access import *
from cobra.mit.session import *
from cobra.model.ipv4 import *
import cobra.model.fv
import cobra.model.pol
import cobra.mit.request
import inspect
from argparse import ArgumentParser


class environment():
    def __init__(self):
        '''
        Parses argument list
        '''
        self.host = '172.30.0.168'
        self.user = 'admin'
        self.pw = 'Sigma4290'
        self.tenant = 'Demo'


    def login_to_apic(self, url, username, password):
        '''
        log into an APIC and create a directory object
        :param username:
        :param password:
        '''
        if 'http' in url:
            pass
        else:
            url = 'https://' + url

        self.ls = cobra.mit.session.LoginSession(url, username, password)
        self.md = cobra.mit.access.MoDirectory(self.ls)
        self.md.login()

    def check_tenant(self):
        '''
        Checks tenant name to if there is a match
        '''
        bds = self.md.lookupByClass("fvBD", parentDn="uni/tn-" + self.tenant)
        if len(bds) == 0:
            print '\nNo matching tenant found or tenant empty'
            exit()




    def get_data(self):
        '''
        Checks tenant name and if there is a match, outputs the BDs under that tenant.
        This is used when the --leak option is not present.
        '''

        # Check tenant name against APIC
        self.check_tenant()
        output = ''
        bds = self.md.lookupByClass("fvBD", parentDn = "uni/tn-" + self.tenant)
        for bd in bds:
             output += '\n+' + str(bd.rn)
             subnets = self.md.lookupByClass("fvSubnet", parentDn = bd.dn)
             for subnet in subnets:
                 output += '\n+-' + subnet.ip + ' scope: ' + subnet.scope
        print output






if __name__ == '__main__':
    # Disable SSL warnings
    requests.packages.urllib3.disable_warnings()

    env = environment()
    # Login to APIC
    env.login_to_apic(env.host, env.user, env.pw)
    env.get_data()





