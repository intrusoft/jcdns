"""

Parse DNS UDP queries and format responses, only UDP for now

"""

import struct
from trafficengine import TrafficEngine

DNS_QTYPES = {1:'A', 2:'NS', 3:'CNAME', 4:'SOA', 5:'PTR', 6:'HINFO', 7:'MX', 8:'TXT'}

# todo: use pointers in rdata

class DNSProcess():
    def __init__(self):
        self._te = TrafficEngine()
      
    def lookup_A(self,q,clientip):
        records = self._te.resolve(q['qname'], clientip)
        return(records)    

    def parse(self,packet):
        dq = {}
        dq['id'] = struct.unpack('>H', packet[:2])[0]
        dq['qr'] = (ord(packet[2]) >> 7) 
        dq['opcode'] = (ord(packet[2]) >> 3) & 15
        dq['aa'] = (ord(packet[2]) >> 2) & 1 
        dq['tc'] = (ord(packet[2]) >> 1) & 1
        dq['rd'] = ord(packet[2]) & 1   
        dq['z'] = (ord(packet[3]) >> 4) & 7
        dq['rcode'] = ord(packet[3]) & 15
        dq['qdcount'] = struct.unpack('>H', packet[4:6])[0] 
        dq['ancount'] = struct.unpack('>H', packet[6:8])[0]
        dq['nscount'] = struct.unpack('>H', packet[8:10])[0]
        dq['arcount'] = struct.unpack('>H', packet[10:12])[0]

        qdlen = ord(packet[12])
        offset = 13 

        labels = []  
        while True:
           label = packet[offset:offset+qdlen]
           offset += qdlen
           qdlen = ord(packet[offset:offset+1])
           offset += 1
           labels.append(label)
           if qdlen == 0: break

        dq['qname'] = ".".join(labels).rstrip('.')
        dq['qtype'] = struct.unpack('>H', packet[offset:offset+2])[0]    
    
        offset+= 2
        dq['qclass'] = struct.unpack('>H', packet[offset:offset+2])[0]

        return dq   

    def processquery(self,q, clientip):
        if q['qr'] == 0 and q['opcode'] == 0 and q['qdcount'] == 1:
            #print "query type: %d (%s)"% (q['qtype'], DNS_QTYPES[q['qtype']])

            if q['qtype'] == 1:
               records = self.lookup_A(q, clientip) 

        q['resource_records'] = records  
        print "set rcode to 3"
        q['rcode'] = 0      
        if not records or len(records) == 0:
            q['rcode'] = 3
            

    def genresponse(self, q):
        q['qdcount'] = 0
        if q['resource_records']:
            q['ancount'] = len(q['resource_records'])
        q['qr'] = 1
        q['tc'] = 0
        q['ra'] = 1     #commented this out, maybe this gets rid of the warning

    def packresponse(self, q):
        message = None
        message = struct.pack('>H', q['id'])  #first 16 bites

        _qr = q['qr'] << 7
        _opcode = q['opcode'] << 3
        _aa = q['aa'] << 2
        _tc = q['tc'] << 1
        _rd = q['rd']
        message += struct.pack('>B', (_qr | _opcode | _aa | _tc | _rd))  # next 8 bits

        _ra = q['ra'] << 7
        _z = q['z'] << 4
        _rcode = q['rcode']
        message += struct.pack('>B', (_ra | _z | _rcode))

        message += struct.pack('>H', q['qdcount'])
        message += struct.pack('>H', q['ancount'])
        message += struct.pack('>H', q['nscount'])
        message += struct.pack('>H', q['arcount'])

        # pack resource record data
        if q['resource_records']:
            for rr in q['resource_records']: 
                rawrr = ""
                for n in rr['name'].split('.'):   # this stuff should be replaced with a pointer eventually, maybe scan the message for occurance
                    rawrr += chr(len(n)) + n
                rawrr += '\x00' # label terminator

                rawrr += struct.pack('>H', rr['type'])
                rawrr += struct.pack('>H', rr['class'])
                rawrr += struct.pack('>I', rr['ttl'])

                # todo: what if othan arecord returned
                if rr['type'] == 1:
                    rawrr += "\x00\x04" # rdata len
                    for i in rr['ip'].split('.'):
                        rawrr += chr(int(i))
                message += rawrr
 
        return message

