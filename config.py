"""

Removed Cassandra backend, replaced with simple json format for now

"""

import json

class Config:

   def getconfig(self, domainname):
       # todo: pass in config file
       with open('example.json') as f:
           data = json.load(f)

       if domainname in data:
           return data[domainname]
       else:
           return None

