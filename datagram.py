
from struct import unpack
import socket

class ipv4datagram(object):
    """IP Packet""" 
    
    def __init__(self,src_mac_addr=None,dest_mac_addr=None,eth_protocol=None,packet=None):
        self.data = packet
        self.dest_mac_addr = dest_mac_addr
        self.src_mac_addr = src_mac_addr
        self.eth_protocol = eth_protocol
        self.ip_version = None
        self.ihl = None
        self.ttl = None
        self.protocol = None
        self.source_addr = None
        self.dest_addr = None
        self.id = None
        self.dict = {}
        if packet != None:
            self.parse_ip_packet(packet)

    def fill_dict(self):
        self.dict = { 'dest_mac_addr' : self.dest_mac_addr, 'src_mac_addr': self.src_mac_addr, 'eth_protocol' : self.eth_protocol,
            'ip_version' : self.ip_version, 'ihl' : self.ihl , 'ttl' : self.ttl, 'protocol' : self.protocol, 'source_addr' : self.source_addr,
            'dest_addr' : self.dest_addr
        }
    def parse_ip_packet(self,packet):

        self.data = packet
        #Parse IP header
        #take first 20 characters for the ip header
        eth_length = 14
        ip_header = packet[eth_length:20+eth_length]

        iph = unpack('!BBHHHBBH4s4s' , ip_header)
 
        version_ihl = iph[0]
        self.ip_version = version_ihl >> 4
        self.ihl = version_ihl & 0xF
 
        iph_length = self.ihl * 4
 
        self.ttl = iph[5]
        self.protocol = iph[6]
        self.source_addr = socket.inet_ntoa(iph[8]);
        self.dest_addr = socket.inet_ntoa(iph[9]);

        # print 'Version : ' + str(self.ip_version) + ' IP Header Length : ' + str(self.ihl) + ' TTL : ' + str(self.ttl) + \
        #     ' Protocol : ' + str(self.protocol) + ' Source Address : ' \
        #         + str(self.source_addr) + ' Destination Address : ' + str(self.dest_addr)
        self.fill_dict()
    def getprotocol(self):
        if self.protocol == 6:
            return "TCP"
        elif self.protocol == 1:
            return "ICMP"
        elif self.protocol == 17:
            return "UDP"
        else:
            return None

    def handletcppacket(self):
        if self.protocol != 6 :
            print "Not a Tcp Packet"
            return None

        eth_length = 14
        iph_length = self.ihl * 4

        tcp_packet = tcppacket()

        t = iph_length + eth_length
        tcp_header = self.data[t:t+20]
 
        tcph = unpack('!HHLLBBHHH' , tcp_header)
             
        tcp_packet.source_port = tcph[0]
        tcp_packet.dest_port = tcph[1]
        tcp_packet.sequence = tcph[2]
        tcp_packet.acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcp_packet.tcp_header_length = doff_reserved >> 4
        # print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' \
        #     + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
        h_size = eth_length + iph_length + tcp_packet.tcp_header_length * 4
        data_size = len(self.data) - h_size
        #get data from the packet
        tcp_packet.data = self.data[h_size:]
        return tcp_packet

    def handleicmp(self):
        if self.protocol != 1:
            return None

        icmp_packet = icmppacket()
        eth_length = 14
        iph_length = self.ihl * 4
        u = iph_length + eth_length
        icmph_length = 4
        icmp_header = self.data[u:u+4]
        icmph = unpack('!BBH' , icmp_header)
             
        icmp_packet.icmp_type = icmph[0]
        icmp_packet.code = icmph[1]
        icmp_packet.checksum = icmph[2]
             
        # print 'Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum)
             
        h_size = eth_length + iph_length + icmph_length
        data_size = len(self.data) - h_size     
        #get data from the packet
        icmp_packet.data = self.data[h_size:]
        # print 'Data : ' + data
        return icmp_packet

    def handleudp(self):
        eth_length = 14
        iph_length = self.ihl * 4

        udp_packet = udppacket()
        u = iph_length + eth_length
        udph_length = 8
        udp_header = self.data[u:u+8]

        udph = unpack('!HHHH' , udp_header)
             
        udp_packet.source_port = udph[0]
        udp_packet.dest_port = udph[1]
        udp_packet.length = udph[2]
        udp_packet.checksum = udph[3]
             
        # print 'Source Port : ' + str(source_port) + ' Dest Port : ' \
        #     + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum)
             
        h_size = eth_length + iph_length + udph_length
        data_size = len(self.data) - h_size
        
        #get data from the packet
        udp_packet.data = self.data[h_size:]
        return udp_packet
        # print 'Data : ' + data

class tcppacket(object):
    """Tcp Packet"""
    def __init__(self):
        self.source_port = None
        self.dest_port = None
        self.sequence = None
        self.tcp_header_length = None
        self.acknowledgement = None
        self.packet_data = None


class  icmppacket(object):
    """docstring for  icmppacket"""
    def __init__(self):
        self.icmp_type = None
        self.icmp_code = None
        self.checksum = None
        self.data = None

class udppacket(object):
    """docstring for udp"""
    def __init__(self):
        self.source_port = None
        self.dest_port = None
        self.length = None
        self.checksum = None
        self.data = None

class datamanager(object):
    """Stores Packets in a list"""
    def __init__(self):
        self.packet_list = {}
        self.num_of_packets = 0

    def add_packet(self,packet):
        if isinstance(packet,ipv4datagram):
            self.num_of_packets+=1
            self.packet_list[self.num_of_packets] = packet
            packet.id = self.num_of_packets
    
    def save(self,filehandle):
        newfile=open("sniff_file","wb")
        print "packets",self.num_of_packets
        for key,val in self.packet_list.items():
            newfile.write(val.data)
            newfile.write("\r\n")
            filehandle.write(val.data)
            filehandle.write("\r\n")
            
    def readfile(self,filehandle):
        list_pack = []
        map_pack = []
        if filehandle == None:
            newfile = open("sniff_file","rb")
            block = newfile.read()
            lines = block.split("\r\n")
            print len(lines)
            for line in lines:
                # print line
                list_pack.append(line)
            newfile.close()
        else:
            block = filehandle.read()
            lines = block.split("\r\n")
            print len(lines)
            for line in lines:
                list_pack.append(line)

        list_pack.pop()
        return list_pack
