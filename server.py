"""

Simple code to process one request at a time

"""

from  dnsprocess import DNSProcess
import socket

DNS_PORT = 53

class Base(object):
    def start(self, port=DNS_PORT):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', port))

        d = DNSProcess()

        while True:
            message,address = s.recvfrom(512)
            dnsquery = d.parse(message)
            d.processquery(dnsquery, address[0])
            d.genresponse(dnsquery)
            message = d.packresponse(dnsquery)
            s.sendto(message, address)
        
