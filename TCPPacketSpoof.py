import socket, sys, time, signal, os
from impacket import ImpactPacket
from impacket import ImpactDecoder
from optparse import OptionParser

# Note you need this package to install: http://oss.coresecurity.com/projects/impacket.html

oparser = OptionParser("usage: %prog [options] [command]*", version="v%d.%d.%d" % (1, 0, 0))
oparser.add_option("-d", "--debug", dest="debug", action = "store_true", help="verbose", default=False)
oparser.add_option("-s", "--si", dest="sourceip", help="Source IP adres")
oparser.add_option("-p", "--sp", dest="sourceport", help="Source port", metavar="int")
oparser.add_option("-t", "--ti", dest="targetip", help="Target IP adres")
oparser.add_option("-q", "--tp", dest="targetport", help="Target port", metavar="int")
oparser.add_option("-y", "--syn",dest="syn",help="Syn number",metavar="int", default="0")
oparser.add_option("-a", "--ack", dest="ack", help="ack number", metavar="int", default="0")

#(options,args) = oparser.parse_args(sys.argv)


#================================================================

def fakeConnection((options,args)):
	        
	dhost = options.targetip           	# The remote host
	dport = int(options.targetport) 		# The same port as used by the server
	shost = options.sourceip         	# The source host
	sport = int(options.sourceport)		# The source port
	SYN = int(options.syn)
	ACK = int(options.ack)
	
	# Create a new IP packet and set its source and destination addresses.
	ip = ImpactPacket.IP()
	ip.set_ip_src(shost)
	ip.set_ip_dst(dhost)

	# Create a new TCP
	tcp = ImpactPacket.TCP()
        
	# Set the parameters for the connection
	tcp.set_th_sport(sport)
	tcp.set_th_dport(dport)
	tcp.set_th_seq(SYN)
	tcp.set_SYN()
	if (options.ack > 0):
		tcp.set_th_ack(ACK)
		tcp.set_ACK()
        
        
	# Have the IP packet contain the TCP packet
	ip.contains(tcp)

	# Open a raw socket. Special permissions are usually required.
	protocol_num = socket.getprotobyname('tcp')
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol_num)
	s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
	
	# Calculate its checksum.
	tcp.calculate_checksum()
	tcp.auto_checksum = 1
	
	# Send it to the target host.
	s.sendto(ip.get_packet(), (dhost, dport))
	

fakeConnection(oparser.parse_args(sys.argv))
