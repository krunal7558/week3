
'''
Problem statement :
Using SNMPv3 create two SVG image files.  

The first image file should graph the input and output octets on interface FA4 on pynet-rtr1 every five minutes for an hour. 
Use the pygal library to create the SVG graph file. 
Note, you should be doing a subtraction here (i.e. the input/output octets transmitted during this five minute interval).  

The second SVG graph file should be the same as the first except graph the unicast packets received and transmitted.

The relevant OIDs are as follows:

('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5')
('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5')
('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5')
('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')

'''

#!/usr/bin/env python

import pygal
import pysnmp
from time import sleep
from snmp_helper import snmp_get_oid_v3,snmp_extract
from getpass import getpass

if __name__ == '__main__':
    oids = [('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5'), \
            ('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5'), \
            ('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5'), \
            ('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),\
            ('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')]
    graph1 = pygal.Bar()
    graph2 = pygal.Bar()
    ifInOctets_fa4 = []
    ifInUcastPkts_fa4 = []
    ifOutOctets_fa4 = []
    ifOutUcastPkts_fa4 = []
    graph1.title = 'Fa4 in/out octets in bytes'
    graph2.title = 'Fa4 in/out unicast packets'
    snmp_device = ('184.105.247.71', 161)
    password = getpass()
    a_user = 'pysnmp'
    auth_key = password
    encrypt_key = password
    snmp_user= (a_user, auth_key, encrypt_key)
    duration = range(0,65,5) # [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]

    graph1.x_lables = ['0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
    graph2.x_lables = ['0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
    for min in duration:
        print 'Collecting samples for timeslot ' + str(min/5)
        for oid in oids:
            snmp_data = snmp_get_oid_v3(snmp_device, snmp_user, oid[1])
            if oid[0] == 'ifInOctets_fa4':
                data = int(snmp_extract(snmp_data))
                if min == 0:
                     ifInOctets_fa4.append(0)
                else:
                    ifInOctets_fa4.append(data - ifInOctets)
                ifInOctets = data
            elif oid[0] == 'ifInUcastPkts_fa4':
                data = int(snmp_extract(snmp_data))
                if min == 0:
                    ifInUcastPkts_fa4.append(0)
                else:
                    ifInUcastPkts_fa4.append(data - ifInUcastPkts)
                ifInUcastPkts = data
            elif oid[0] == 'ifOutOctets_fa4':
                data = int(snmp_extract(snmp_data))
                if min == 0:
                     ifOutOctets_fa4.append(0)
                else:
                    ifOutOctets_fa4.append(data - ifOutOctets)
                ifOutOctets = data
            elif oid[0] == 'ifOutUcastPkts_fa4':
                data = int(snmp_extract(snmp_data))
                if min == 0:
                     ifOutUcastPkts_fa4.append(0)
                else:
                     ifOutUcastPkts_fa4.append(data - ifOutUcastPkts)
                ifOutUcastPkts = data
        sleep(300)

    graph1.add('InBytes',ifInOctets_fa4)
    graph1.add('OutBytes',ifOutOctets_fa4)
    graph2.add('InUnicastPackets',ifInUcastPkts_fa4)
    graph2.add('OutUnicastPackets',ifOutUcastPkts_fa4)

    graph1.render_to_file('graph1.svg')
    graph2.render_to_file('graph2.svg')
