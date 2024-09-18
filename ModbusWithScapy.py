# pip install scapy
# Documentation: https://scapy.readthedocs.io/en/latest/installation.html
import struct
from scapy.all import IP, TCP,Raw, send, sr1, sniff, get_if_list
from optparse import OptionParser
import sys

def createModbusReadHoldingRegisterRequest(transaction_id,protocol_identifier,field_length,unit_id,function_code, address,numberOfBytesToRequest):
 # Pack the components into bytes (Note: H=2 bytes unsigned short, B=1 byte unsighed short: https://docs.python.org/3/library/struct.html)
    data = struct.pack(
        '>HHHBBHH',
        transaction_id,
        protocol_identifier,
        field_length,
        unit_id,
        function_code,
        address,
        numberOfBytesToRequest
    ) 
    return data

def handle_response(packet):
    """Callback function to handle the response packet and print the Modbus data."""
    if packet.haslayer(Raw):
        modbus_response_data = packet[Raw].load
        print(f"[*] Received Modbus Response Data: {modbus_response_data.hex()}")
    else:
        print("[!] Received packet without Modbus data")

def listInterfaces():
    print("Listing available interfaces, plz be aware than on windows, you need the \\\\Device\\\\NPF_ prefix")
    interfaces = get_if_list()
    j = 0
    for i in interfaces:
        print(j,": ",i)
        j+=1

def sendModbusPackageAndCaptureResponse():
    # Define the IP and TCP headers with adjusted window size and scaling
    ip = IP(src=options.sourceip, dst=options.targetip)

    # Adjust window size to 64240, and set scale=8 to get ws=256
    tcp_syn = TCP(sport=options.sourceport, dport=options.targetport, flags="S", seq=1000, options=[("MSS", 1460), ("SAckOK", ""), ("WScale", 8)], window=64240)
    syn_ack = sr1(ip / tcp_syn)

    if syn_ack:
        print("[*] SYN-ACK received, now sending Modbus request")

        # Send ACK to complete the handshake
        tcp_ack = TCP(sport=options.sourceport, dport=options.targetport, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1, window=64240)
        send(ip / tcp_ack)

        # This is where the modbus magic happens :)
        modbus_data = createModbusReadHoldingRegisterRequest(1234, 0, 6, 1, 0x03, 1, 1)

        # Send the Modbus request with PSH (Push data to application layer, as soon as received) and ACK flags (important!)
        tcp_modbus = TCP(sport=options.sourceport, dport=options.targetport, flags="PA", seq=syn_ack.ack, ack=syn_ack.seq + 1, window=64240)
        data = Raw(load=modbus_data)
        packet = ip / tcp_modbus / data

        send(packet)
        
        myFilter = "tcp and host " + options.targetip + " and port " + str(options.targetport)
        myIface = "\\Device\\NPF_{" + options.ifaceGUID + "}"
        sniff(filter=myFilter, iface=myIface, count=1, prn=handle_response)
    else:
        print("[!] No SYN-ACK received")

# Main program
oparser = OptionParser("usage: %prog [options] [command]*", version="v%d.%d.%d" % (1, 0, 0))
oparser.add_option("-l", "--list", dest="linterfaces", action = "store_true", help="List available interfaces", default=False)
oparser.add_option("-s", "--si", dest="sourceip", help="Source IP adres", default="192.168.0.2")
oparser.add_option("-p", "--sp", dest="sourceport", help="Source port", metavar="int", default=1336)
oparser.add_option("-t", "--ti", dest="targetip", help="Target IP adres", default="192.168.0.3")
oparser.add_option("-q", "--tp", dest="targetport", help="Target port", metavar="int", default=510)
oparser.add_option("-g", "--ag", dest="ifaceGUID", help="Adapter GUID (prefixes and {} will be added as part of the script", default="00000000-0000-0000-0000-000000000000")
(options,args) = oparser.parse_args(sys.argv)

if(options.linterfaces):
    listInterfaces()
else:
        sendModbusPackageAndCaptureResponse()
    

