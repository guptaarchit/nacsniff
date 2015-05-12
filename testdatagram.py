from sniffer_socket import sniffer

from datagram import ipv4datagram,datamanager

foo = datamanager()
sniffer_obj = sniffer('lo')
list_ = foo.readfile()

for item in list_:
	sniffer_obj.parse_ethernet_header(item)
