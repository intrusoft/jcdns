""" Implement business logic for how to respond to queries and shape traffic """

import random
from config import Config

DEFAULT_TTL = 300

class TrafficEngine():
   
    def __init__(self):
        self._v = Config()
    
    def calculate_round_robin(self, qname, vconfig):
        records = []
        serverchoice = random.randint(0,len(vconfig['servers'])-1)
        # just pluck one of the servers at random
        records.append({'ip':vconfig['servers'][serverchoice]['ip'], 'ttl':DEFAULT_TTL, 'type':1, 'name':qname, 'class':1})
        return records         

    # this percent could be used to do health balancing if something exterior modifies these numbers based on server load             
    def calculate_percent(self, qname, vconfig):
        records = []
        oddsmap = []
        for server in vconfig['servers']:
            oddsmap += [server['ip']] * server['percent']
        choosenip = random.choice(oddsmap)
        records.append({'ip':choosenip, 'ttl':DEFAULT_TTL, 'type':1, 'name':qname, 'class':1})
        return records

    def resolve(self, qname, clientip):
        records = None
        print "qname: %s" % qname
        
        domain = ''
        for x in qname.lower().split('.')[::-1]:
            domain = ".".join([x,domain]).rstrip('.')
            
            print "Trying: ", domain

            try:
                vconfig = self._v.getconfig(domain)
                print vconfig
                if vconfig:
                    # scrub out servers are out of rotation
                    vconfig['servers'] = [n for n in vconfig['servers'] if n['rotation'] == 'on']

                    if vconfig['scheduler'] == 'rr':
                            records = self.calculate_round_robin(qname, vconfig)

                    if vconfig['scheduler'] == 'percent':
                        records = self.calculate_percent(qname, vconfig)
                    break

            except Exception, e:
                raise
                print "problem with getting vip config or server records"
                print str(e)
                records = None

        return(records) 

