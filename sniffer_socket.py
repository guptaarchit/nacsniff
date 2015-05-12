import socket
import sys
import netifaces
from time import sleep
import ctypes
import fcntl
import select
from struct import unpack
import event


#testing ----
from datagram import ipv4datagram
#----

class interfaces(object):
    """Returns interfaces list and fetches IPs associated with them"""
    _interface_list = []

    def __init__(self):
        self._interface_list = netifaces.interfaces()

    def get_interface_list(self):
        return self._interface_list

    def get_interface_addr(self, inface):
        if inface not in self._interface_list:
            print "No Interface found"
            return ""
        else:
            addrs = netifaces.ifaddresses(inface)
            return addrs[netifaces.AF_INET][0]['addr']

    def interface_exists(self, interface):
        if interface in self._interface_list:
            return True
        else:
            return False


class sockets(object):
    """docstring for sockets"""

    def __init__(self):
        pass
        # self.sock = arg

    def get_socket(self, interface):
        try:
            self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003)) 
            self.sock.bind((interface,0))
            #Should the above be changed to smth like socket.IPPROTO_IP but we are receiving ARP and other messages;
        except socket.error , msg:
            print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit(1)

        return self.sock

class ifreq(ctypes.Structure):
    _fields_ = [("ifr_ifrn", ctypes.c_char * 16),
                ("ifr_flags", ctypes.c_short)]


class sniffer(object):
    """docstring for sniffer"""
    sock_o = sockets()
    IFF_PROMISC = 0x100
    SIOCGIFFLAGS = 0x8913
    SIOCSIFFLAGS = 0x8914
    _interface = ""
    interface_ob = interfaces()
    
    event_packet_is_received = event.Event("A packet is received")

    def __init__(self,interface):
        self.sock = self.sock_o.get_socket(interface)
        if self.interface_ob.interface_exists(interface):
            self._interface = interface
        else:
            print "Please give a suitable interface !!"
            sys.exit(1)
        # self.sock.setsockopt(socket.SOL_SOCKET, 25 , interface+'\0')
        self.sock.setblocking(False)
        self.running = False
        print "Sniffer Initiliased"
        # self.sock.bind(('',50000))

    def packetisreceived(self,packet):
        # Do some actions and fire event.
        self.event_packet_is_received(packet)

    def eth_addr (self,a) :
      b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
      return b

    def start_promisc(self):
        """Start promisious mode"""
        try:
            p_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error , msg:
            print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit(1)

        ifr = ifreq()
        ifr.ifr_ifrn = self._interface
        try:
            fcntl.ioctl(p_sock.fileno() ,self.SIOCGIFFLAGS ,ifr)
        except IOError, msg :
            print "Wrong interface!! Error code" + str(msg[0]) + 'Message' + msg[1]
            sys.exit(1)
        ifr.ifr_flags |= self.IFF_PROMISC
        fcntl.ioctl(p_sock.fileno(), self.SIOCSIFFLAGS, ifr) # S for Set
        p_sock.close()

    def close_promisc(self):
        """close promisious mode"""
        try:
            p_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error , msg:
            print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit(1)

        ifr = ifreq()
        ifr.ifr_ifrn = self._interface
        try:
            fcntl.ioctl(p_sock.fileno() ,self.SIOCGIFFLAGS ,ifr)
        except IOError, msg :
            print "Wrong interface!! Error code" + str(msg[0]) + 'Message' + msg[1]
            sys.exit(1)

        ifr.ifr_flags &= ~self.IFF_PROMISC
        fcntl.ioctl(p_sock.fileno(), self.SIOCSIFFLAGS, ifr)
        p_sock.close()

    def parse_ethernet_header(self,packet):
        """
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |       Ethernet destination address (first 32 bits)            |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        | Ethernet dest (last 16 bits)  |Ethernet source (first 16 bits)|
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |       Ethernet source address (last 32 bits)                  |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |        Type code              |                               |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+    
        """
        #parse ethernet header
        eth_length = 14 #Size of header is 14 bytes         
        eth_header = packet[:eth_length]
        eth = unpack('!6s6sH' , eth_header)
        #6s for 6 char[] array
        #H for unsigned short
        eth_protocol = socket.ntohs(eth[2])
        dest_mac = self.eth_addr(packet[0:6])
        source_mac = self.eth_addr(packet[6:12])
        print 'Destination MAC : ' + dest_mac + ' Source MAC : '+ source_mac + ' Protocol : ' + str(eth_protocol)
        return dest_mac, source_mac, eth_protocol

    def parse_ip_packet(self,packet):
        #Parse IP header
        #take first 20 characters for the ip header
        eth_length = 14
        ip_header = packet[eth_length:20+eth_length]

        iph = unpack('!BBHHHBBH4s4s' , ip_header)
 
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
 
        iph_length = ihl * 4
 
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);
 
        print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' \
            + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)

        if protocol == 6:
            self.parse_tcp(packet,iph_length)
        elif protocol == 1:
            self.parse_icmp(packet,iph_length)
        elif protocol == 17:
            self.parse_udp(packet,iph_length)
        else:
            print("Other packet than tcp/udp/icmp")

    def parse_tcp(self,packet,iph_length):
        eth_length = 14
        t = iph_length + eth_length
        tcp_header = packet[t:t+20]
 
        tcph = unpack('!HHLLBBHHH' , tcp_header)
             
        source_port = tcph[0]
        dest_port = tcph[1]
        sequence = tcph[2]
        acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcph_length = doff_reserved >> 4
        print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' \
            + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
        h_size = eth_length + iph_length + tcph_length * 4
        data_size = len(packet) - h_size
        #get data from the packet
        data = packet[h_size:]     
        print 'Data : ' + data

    def parse_icmp(self,packet,iph_length):
        eth_length = 14
        u = iph_length + eth_length
        icmph_length = 4
        icmp_header = packet[u:u+4]
        icmph = unpack('!BBH' , icmp_header)
             
        icmp_type = icmph[0]
        code = icmph[1]
        checksum = icmph[2]
             
        print 'Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum)
             
        h_size = eth_length + iph_length + icmph_length
        data_size = len(packet) - h_size     
        #get data from the packet
        data = packet[h_size:]
        print 'Data : ' + data

    def parse_udp(self,packet,iph_length):
        eth_length = 14
        u = iph_length + eth_length
        udph_length = 8
        udp_header = packet[u:u+8]

        udph = unpack('!HHHH' , udp_header)
             
        source_port = udph[0]
        dest_port = udph[1]
        length = udph[2]
        checksum = udph[3]
             
        print 'Source Port : ' + str(source_port) + ' Dest Port : ' \
            + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum)
             
        h_size = eth_length + iph_length + udph_length
        data_size = len(packet) - h_size
             
        #get data from the packet
        data = packet[h_size:]
             
        print 'Data : ' + data

    def start(self):
        input_list = [self.sock,sys.stdin]
        self.running = True
        self.start_promisc()
        while self.running:
            inputready,outputready,exceptready = select.select(input_list,[],[])
            for s in inputready:

                if s == self.sock:
                    try:
                        packet = self.sock.recvfrom(65565);    
                    except socket.timeout, e:
                        err = e.args[0]
                        # this next if/else is a bit redundant, but illustrates how the
                        # timeout exception is setup
                        if err == 'timed out':
                            sleep(1)
                            print 'recv timed out, retry later'
                            continue
                        else:
                            print e
                            # continue
                            sys.exit(1)
                    except socket.error, e:
                        print e
                        sys.exit(1)
                    else:
                        # forward packet
                        sender = packet[0]
                        packet = packet[0]

                        dest_mac, source_mac, eth_protocol = self.parse_ethernet_header(packet)
                        # self.packetisreceived(eth_protocol)

                        if eth_protocol == 8:
                            print "IP Packet"
                            #ip_packet = ipv4datgram(packet)
                            #ip_packet.parse_ip_packet()

                            self.parse_ip_packet(packet)
                            ip_packet = ipv4datagram(source_mac,dest_mac,eth_protocol,packet)
                            ip_packet.parse_ip_packet(packet)
                            #fire event
                            #self.packetisreceived(ip_packet)
                            self.packetisreceived(ip_packet)

                        # self.running = False
                        # break
                        # continue
                if s  == sys.stdin:
                    dummy = sys.stdin.readline()
                    running = False
                else:
                    continue

        self.close_promisc()
        self.sock.close()

    def _start(self):
        print "Sniffer Started"
        self.running = True

    def close(self):
        print "Close Called"
        print self.running
        if self.running == True:
            self.running = False
            self.close_promisc()
            self.sock.close()
            print "Sniffer Closed"

    def _close(self):
        print "Sniffer Closed"
        self.running = False

###Debug

if __name__ == "__main__":
    x = interfaces()
    print x.get_interface_list()
    print x.get_interface_addr('wlan0')
    sniff = sniffer('wlan0')
    sniff.start()
    # sniff.start_promisc('eth0')
    # raw_input()
    # sniff.close_promisc()