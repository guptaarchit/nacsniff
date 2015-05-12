#!/usr/bin/env python

import nmap
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import math
from datetime import datetime
import os
def long2net(arg):
    if (arg <= 0 or arg >= 0xFFFFFFFF):
        raise ValueError("illegal netmask value", hex(arg))
    return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))


def to_CIDR_notation(bytes_network, bytes_netmask):
    network = scapy.utils.ltoa(bytes_network)
    netmask = long2net(bytes_netmask)
    net = "%s/%s" % (network, netmask)
    if netmask < 16:
        logger.warn("%s is too big. skipping" % net)
        return None

    return net
host_count=0
def callback_result(host,scan_result):
    # print "---------------------"
    # print host,scan_result
    global host_count
    if scan_result['nmap']['scanstats']['uphosts'] != '0':
        print host,scan_result
        host_count+=1
        print host_count
def main():
    hosts_list = []
    for network, netmask, _, interface, address in scapy.config.conf.route.routes:

        # skip loopback network and default gateway
        if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
            continue

        if netmask <= 0 or netmask == 0xFFFFFFFF:
            continue

        net = to_CIDR_notation(network, netmask)

        if interface != scapy.config.conf.iface:
            # see http://trac.secdev.org/scapy/ticket/537
            print("skipping %s because scapy currently doesn't support arping on non-primary network interfaces", net)
            continue

        if net:
            print "Arping" ,net ,"on",interface
            # nm = nmap.PortScannerAsync()
            nm = nmap.PortScanner()
            t1 = datetime.now()
            # nm.scan(hosts=net,arguments="-n -sP -T4  --max-rtt-timeout 200ms", callback=callback_result)
            nm.scan(hosts=net,arguments="-n -sP -T4  --max-rtt-timeout 200ms")
            #print nm.scaninfo()
            #or maybe this
            # hosts_list = [(x, nm[x]['status']['state'],nm[x].hostname()) for x in nm.all_hosts()]
            # for host, status in hosts_list:
            #   print('{0}:{1}'.host)

            # host_count = 0
            # while nm.still_scanning():
            #     print "Waiting>>"
            # nm.wait(timeout=65)
            
            # global host_count
            last_host = ""
            for host in nm.all_hosts():
                print('----------------------------------------------------')
                print('Host : {0} ({1})'.format(host, nm[host].hostname()))
                print('State : {0}'.format(nm[host].state()))
                # host_count+=1
                for proto in nm[host].all_protocols():
                    print('----------')
                    print('Protocol : {0}'.format(proto))

                    lport = list(nm[host][proto].keys())
                    lport.sort()
                    for port in lport:
                        print('port : {0}\tstate : {1}'.format(port, nm[host][proto][port])) 
                        if port == "mac":
                            hosts_list.append((host,nm[host].state(),nm[host].hostname(),nm[host][proto][port]))

                last_host = host       
            print host_count
            print hosts_list[0]
            t2 = datetime.now()

            # Calculates the difference of time, to see how long it took to run the script
            total =  t2 - t1

            # Printing the information to screen
            print 'Scanning Completed in: ', total
            
    return hosts_list

def get_port_scan(host):
    nm = nmap.PortScanner()
    if (os.getuid() == 0):
        nm.scan(host, arguments='-sS -vv -n -PN --max-rtt-timeout 500ms -T4 -A -p 22-1000')      # scan host ports from 22 to 1000
        print nm.scaninfo()
        for host in nm.all_hosts():
            if 'osclass' in nm[host]:
                for osclass in nm[host]['osclass']:
                    print('OsClass.type : {0}'.format(osclass['type']))
                    print('OsClass.vendor : {0}'.format(osclass['vendor']))
                    print('OsClass.osfamily : {0}'.format(osclass['osfamily']))
                    print('OsClass.osgen : {0}'.format(osclass['osgen']))
                    print('OsClass.accuracy : {0}'.format(osclass['accuracy']))
                    print('')

            if 'osmatch' in nm[host]:
                for osmatch in nm[host]['osmatch']:
                    print('OsMatch.name : {0}'.format(osmatch['name']))
                    print('OsMatch.accuracy : {0}'.format(osmatch['accuracy']))
                    print('OsMatch.line : {0}'.format(osmatch['line']))
                    print('')

            if 'hostscript' in nm[host]:
                for hscript in nm[host]['hostscript']:
                    print('HostScript Results : {0}'.format(hscript['output']))
        
            for proto in nm[host].all_protocols():
                print('----------')
                print('Protocol : {0}'.format(proto))
                print nm[host][proto]

                if proto == "addresses" or proto == "tcp" or proto == "udp":
                    lport = list(nm[host][proto].keys())
                    lport.sort()
                    for port in lport:
                        print('port : {0}\tstate : {1}'.format(port, nm[host][proto][port]))
            print nm[host].all_tcp()           # get all ports for tcp protocol (sorted version)
            print nm[host].all_udp()           # get all ports for udp protocol (sorted version)

if __name__ == "__main__":
    # main()
    get_port_scan('172.16.101.197')
