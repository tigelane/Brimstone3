import json
import re
import acitoolkit.acitoolkit as aci
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware


class BeakerSessionInterface(SessionInterface):
    def open_session(self, app, request):
        if request.environ.has_key('beaker.session'):
            return request.environ['beaker.session']

    def save_session(self, app, session, response):
        session.save()


class Beaker(object):
    def __init__(self, app=None, session_timeout=600):
        if app is not None:
            self.init_app(app, session_timeout)
        else:
            self.app = None

    def init_app(self, app, session_timeout):
        app.config.setdefault('BEAKER_SESSION_TYPE', 'memory')
        app.config.setdefault('BEAKER_SESSION_URL', None)
        app.config.setdefault('BEAKER_SESSION_DATA_DIR', './.beaker-session')
        app.config.setdefault('BEAKER_SESSION_COOKIE_EXPIRES', True)
        app.config.setdefault('BEAKER_SESSION_TIMEOUT', session_timeout)
        self.app = app
        self._set_beaker_session()

    def _set_beaker_session(self):
        session_opts = {
            'session.type': self.app.config['BEAKER_SESSION_TYPE'],
            'session.data_dir': self.app.config['BEAKER_SESSION_DATA_DIR'],
            'session.url': self.app.config['BEAKER_SESSION_URL'],
            'session.cookie_expires': self.app.config['BEAKER_SESSION_COOKIE_EXPIRES'],
            'session.timeout': self.app.config['BEAKER_SESSION_TIMEOUT']
        }

        self.app.wsgi_app = SessionMiddleware(self.app.wsgi_app, session_opts)
        self.app.session_interface = BeakerSessionInterface()

class Endpoint():
    def __init__(self, mac_address):
        self.mac = mac_address

class EPGMap:
    def __init__(self, parent_tenant, parent_apn):
        self.name = ''
        self.parent_tenant = parent_tenant
        self.parent_apn = parent_apn
        self.provided_contracts = {}
        self.consumed_contracts = {}
        self.provider_endpoints = {}
        self.consumer_endpoints = {}

class ContractMap:
    def __init__(self):
        self.names = []
        self.filters = {}
        self.tenant = {}

class URIBMap:
    def __init__(self, ep):
        self.endpoint = ep


def identify(input):
    """
    Determines what type of data is in use.
    :param input: Data which needs to be identified
    :return: output - Classification data submitted
    """
    output = 'unknown'
    # Checks for IP Address
    m = re.search('[1-2]?[0-9]?[0-9]?\.[1-2]?[0-9]?[0-9]?\.[1-2]?[0-9]?[0-9]?\.[1-2]?[0-9]?[0-9]?', input)
    if m:
        output = 'ipAddress'

    # Checks for Cisco style MAC Address
    m = re.search(
        '[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f]\.[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f]\.[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f]\.[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f]',
        input)
    if m:
        output = 'macAddress4'

    # Checks for MS style MAC Address
    m = re.search(
        '[0-9,a-f][0-9,a-f]:[0-9,a-f][0-9,a-f]:[0-9,a-f][0-9,a-f]:[0-9,a-f][0-9,a-f]:[0-9,a-f][0-9,a-f]:[0-9,a-f][0-9,a-f]',
        input.lower())
    if m:
        output = 'macAddress2'

    # Checks for ACI Encapsulation
    m = re.search('vlan-', input.lower())
    if m:
        output = 'encap'

    return output

def get_epg_info(session, tenant, app, epg):
    endpoints = []
    url = '/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json?query-target=children&target-subtree-class=fvCEp&rsp-subtree=children&rsp-subtree-class=fvRsVm,fvRsHyper,fvRsCEpToPathEp,fvIp,fvReportingNode' % (tenant, app, epg)
    resp = session.get(url)
    dns = json.loads(resp.text)['imdata']


    for dn in dns:
        ips = [dn['fvCEp']['attributes']['ip']]
        paths = []
        children = dn['fvCEp']['children']
        for child in children:
            try:
                ips.append(child['fvIp']['attributes']['addr'])
            except:
                pass

            try:
                mac = dn['fvCEp']['attributes']['mac']
                encap = dn['fvCEp']['attributes']['encap']
            except:
                pass



            try:
                paths.append(child['fvRsCEpToPathEp']['attributes']['tDn'])
            except:
                pass

        for ip in ips:
            EP = Endpoint(mac)
            EP.ip = ip
            EP.encap = encap
            EP.if_name = ''
            for path in paths:
                m = re.search('paths-([0-9\-]*)/pathep-\[([a-zA-Z0-9\-\/]*)\]', path)
                if m:
                    EP.if_name += 'Nodes-%s/%s\r\n' % (m.group(1),m.group(2))
                else:
                    print 'not found', path

            endpoints.append(EP)

    return endpoints


def get_epg_pctag(session, epg):
    url = '/api/node/class/fvAEPg.json?query-target-filter=and(eq(fvAEPg.name,"%s"))' % (epg)
    resp = session.get(url)
    dn = json.loads(resp.text)['imdata'][0]
    pcTag = dn['fvAEPg']['attributes']['pcTag']
    return pcTag

def get_pctag_endpoints(session, pcTag):
    # endpoints = []
    url = '/api/node/class/fvAEPg.json?query-target-filter=and(eq(fvAEPg.pcTag,"%s"))' % (pcTag)
    resp = session.get(url)
    dns = json.loads(resp.text)['imdata']
    for dn in dns:
        print dn


def get_all_vzRtProv(session, contract):
    """
    Get vzRsAnyToConss and add to dictionary
    :return: vzRtProvs
    """

    vzRtProvs = {}
    url = '/api/node/class/vzRtProv.json?query-target-filter=and(eq(vzRtProv.tCl,"l3extInstP"))'
    resp = session.get(url)
    results = json.loads(resp.text)['imdata']
    for result in results:
        dn = result['vzRtProv']['attributes']['dn']
        m = re.search('uni/tn-([a-zA-Z0-9\-]*)/brc-([a-zA-Z0-9\-]*)/', dn)
        if m:
            contract = m.group(1) + '/' + m.group(2)
        else:
            print 'Error in get_all_vzRtProv()'

        tDn = result['vzRtProv']['attributes']['tDn']
        m = re.search('uni/tn-([a-zA-Z0-9\-]*)/out-([a-zA-Z0-9\-]*)/instP-([a-zA-Z0-9\-]*)', tDn)
        if m:
            l3Out = m.group(2) + '/' + m.group(3)
            vzRtProvs[contract] = l3Out
        else:
            print 'Error in get_all_vzRtProv()'


    return vzRtProvs

def get_all_vzRtCons(session, contract):
    """
    Get vzRsAnyToConss and add to dictionary
    :return: vzRtConss
    """

    vzRtConss = {}
    url = '/api/node/class/vzRtCons.json?query-target-filter=and(eq(vzRtCons.tCl,"l3extInstP"))'
    resp = session.get(url)
    results = json.loads(resp.text)['imdata']
    for result in results:
        dn = result['vzRtCons']['attributes']['dn']
        m = re.search('uni/tn-([a-zA-Z0-9\-]*)/brc-([a-zA-Z0-9\-]*)/', dn)
        if m:
            contract = m.group(1) + '/' + m.group(2)
        else:
            print 'not found'

        tDn = result['vzRtCons']['attributes']['tDn']
        m = re.search('uni/tn-([a-zA-Z0-9\-]*)/out-([a-zA-Z0-9\-]*)/instP-([a-zA-Z0-9\-]*)', tDn)
        if m:
            l3Out = m.group(2) + '/' + m.group(3)
            vzRtConss[contract] = l3Out
        else:
            print 'not found'

    return vzRtConss

def get_all_RsAnyToProv(session):
    """
    Get vzRsAnyToProvs and add to dictionary
    :return: vzRsAnyToProvs
    """
    vzRsAnyToProvs = {}
    url = '/api/node/class/vzRsAnyToProv.json'
    resp = session.get(url)
    results = json.loads(resp.text)['imdata']
    for result in results:
        name = result['vzRsAnyToProv']['attributes']['tnVzBrCPName']
        dn = result['vzRsAnyToProv']['attributes']['dn']
        vzRsAnyToProvs[name] = dn
    return vzRsAnyToProvs

def get_all_RsAnyToCons(session):
    """
    Get vzRsAnyToConss and add to dictionary
    :return: vzRsAnyToProvs
    """

    vzRsAnyToConss = {}
    url = '/api/node/class/vzRsAnyToCons.json'
    resp = session.get(url)
    results = json.loads(resp.text)['imdata']
    for result in results:
        name = result['vzRsAnyToCons']['attributes']['tnVzBrCPName']
        dn = result['vzRsAnyToCons']['attributes']['dn']
        vzRsAnyToConss[name] = dn
    return vzRsAnyToConss

def get_bd_from_subnet(session, route):
    '''
    Compares gateway IP and route to see if BD is a match.
    :param subnet:
    :return:
    '''

    bd_name = 'Error'
    tenants = get_user_tenants()
    for tenant in tenants:
        if tenant.name not in ('infra', 'mgmt'):
            apps = aci.AppProfile.get(session, tenant)
            for app in apps:
                bds = aci.BridgeDomain.get(session, tenant)
                for bd in bds:
                    subnets = aci.Subnet.get(session, bd, tenant)
                    for subnet in subnets:
                        network = ipaddress.IPv4Interface(subnet.ip.decode('utf-8')).network.with_prefixlen
                        test = ipaddress.IPv4Interface(route).network.with_prefixlen
                        if test == network:
                            return 'BD:' + bd.name


    return bd_name


def get_node_health(session, node_dn):
    """
    This will get the health of the switch node
    """
    health = 'Error'
    url = '/api/mo/' + node_dn + \
                   '/sys.json?&rsp-subtree-include=stats&rsp-subtree-class=fabricNodeHealth5min'
    resp = session.get(url)
    results = resp.json()['imdata']
    # print results
    if results:
        try:
            health = results[0]['topSystem']['children'][0]['fabricNodeHealth5min']['attributes']['healthLast']
        except Exception as e:
            print e
    return health

def get_cluster_health(session):
    cluster_info = []
    url = '/api/node/mo/topology/pod-1/node-1/av.json?query-target=children&target-subtree-class=infraWiNode'
    resp = session.get(url)
    results = resp.json()['imdata']

    for result in results:
        nodeName = result['infraWiNode']['attributes']['nodeName']
        adminSt = result['infraWiNode']['attributes']['adminSt']
        # serial = result['infraWiNode']['attributes']['mbSn']
        health = result['infraWiNode']['attributes']['health']
        if health == 'fully-fit':
            health_color = 'green'
        else:
            health_color = 'red'
        cluster_info.append((nodeName, adminSt, health, health_color))
    return cluster_info

def get_system_health(session):
    """
    This will get the health of the switch node
    """
    health = 'Error'
    url = '/api/node/mo/topology/health.json'
    resp = session.get(url)
    results = resp.json()['imdata']
    if results:
        try:
            health = results[0]['fabricHealthTotal']['attributes']['cur']
        except Exception as e:
            print e
    return health

def get_fabric_profile_detail(session):
    """
    Pulls switch profile, interface profile, port info, and policy group from fabric and combines into one view.
    :param session:
    :return:
    """
    profile_details = []
    url = '/api/node/mo/uni/infra.json?query-target=subtree&target-subtree-class=infraNodeP'
    resp = session.get(url)
    switch_profiles = resp.json()['imdata']
    for switch_profile in switch_profiles:
        infraNodePdn = switch_profile['infraNodeP']['attributes']['dn']
        switch_profile_name = switch_profile['infraNodeP']['attributes']['name']
        url = '/api/node/mo/' + infraNodePdn + '.json?query-target=children&target-subtree-class=infraRsAccPortP'
        resp = session.get(url)
        interface_profiles = resp.json()['imdata']
        for interface_profile in interface_profiles:
            try:
                infraRsAccPortPtDn = interface_profile['infraRsAccPortP']['attributes']['tDn']
                m = re.search('accportprof-([a-zA-Z0-9\-\_]*)', infraRsAccPortPtDn)
                if m:
                    interface_profile_name = m.group(1)
                else:
                    print 'not found', infraRsAccPortPtDn

                url = '/api/node/mo/' + infraRsAccPortPtDn + '.json?query-target=subtree&target-subtree-class=infraPortBlk'

                resp = session.get(url)
                ports = resp.json()['imdata']
                for port in ports:
                    infraPortBlkdn = port['infraPortBlk']['attributes']['dn'][:-15]
                    toPort = port['infraPortBlk']['attributes']['toPort']
                    fromPort = port['infraPortBlk']['attributes']['fromPort']
                    if fromPort == toPort:
                        portList = fromPort
                    else:
                        portList = fromPort + '-' + toPort

                    m = re.search('hports-([a-zA-Z0-9\-\_]*)', infraPortBlkdn)
                    if m:
                        port_name = m.group(1)[:-10]
                    else:
                        print 'not found', policy_group

                    url = '/api/node/mo/' + infraPortBlkdn + '.json?query-target=children&target-subtree-class=infraRsAccBaseGrp'
                    resp = session.get(url)

                    groups = resp.json()['imdata']
                    # print groups
                    for group in groups:
                        infraRsAccBaseGrptDn = group['infraRsAccBaseGrp']['attributes']['tDn']
                        m = re.search('accportgrp-([a-zA-Z0-9\-\_]*)', infraRsAccBaseGrptDn)
                        if m:
                            policy_group = m.group(1)
                        else:
                            print 'not found', policy_group


                profile_details.append((interface_profile_name, switch_profile_name, port_name, portList, policy_group))

            except:
                pass




    return profile_details


def get_health_color(score):
    """
    Set font color
    :param score:
    :return:
    """
    color = 'green'
    if int(score) <= 89:
        color = 'orange'
    if int(score) <= 69:
        color = 'red'
    return color

def clean_username(username):
    """
    Strips domain info if default login domain wasn't used.

    :param username: full username
    :return: username with stripped domain
    """
    if "\\\\" in username:
        result = username.split('\\\\')[1]
    else:
        result = username
    return result



def get_node_from_endpoint(session, endpoint_name):

    # # Get BD for EPG
    # resp = session.get('/api/node/mo/uni/tn-' + tenant_name + '/ap-' + apn_name + '/epg-' + epg_name + '/rsbd.json')
    # dn = json.loads(resp.text)['imdata'][0]
    # EPG.endpoint_bd = dn['fvRsBd']['attributes']['tRn'][3:]
    #
    # # Get VRF for BD
    # resp = session.get('/api/node/mo/uni/tn-' + tenant_name + '/BD-' + EPG.endpoint_bd + '/rsctx.json?query-target=self')
    # dn = json.loads(resp.text)['imdata'][0]
    # EPG.endpoint_vrf = dn['fvRsCtx']['attributes']['tRn'][4:]

    # Get fcCEp.dn for Endpoint
    resp = session.get('/api/node/class/fvCEp.json?query-target-filter=and(eq(fvCEp.name,"' + endpoint_name + '"))')
    dn = json.loads(resp.text)['imdata'][0]
    print dn
    endpoint_dn = dn['fvCEp']['attributes']['dn']

    # Get fvIP for Endpoint
    resp = session.get('/api/node/mo/' + endpoint_dn + '.json?query-target=children?query-target-filter=and(eq(fvReportingNode.lcC,"learned"))')
    dns = json.loads(resp.text)['imdata']
    # Find lcC of learned to identify endpoint as attached
    for dn in dns:
        try:
            fvIpdn = dn['fvIp']['attributes']['dn']
        except:
            pass

        # Use lcC to find attached node ID
        resp = session.get('/api/node/mo/' + fvIpdn + '.json?query-target=children')
        dn = json.loads(resp.text)['imdata'][0]
        endpoint_node = dn['fvReportingNode']['attributes']['id']




    resp = session.get(
        '/api/mo/topology/pod-1/node-' + endpoint_node + '.json?query-target=children&target-subtree-class=topSystem')
    dn = json.loads(resp.text)['imdata'][0]
    endpoint_node_oob = dn['topSystem']['attributes']['oobMgmtAddr']

    return endpoint_node, endpoint_node_oob