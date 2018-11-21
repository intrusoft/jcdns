"""

Removed Cassandra backend, replaced with simple json format for now

"""

import json
import os

configfile = 'example.json'

class Config:
   def __init__(self):
       self.running_config = None
       self.config_time = 0

   def getconfig(self, domainname):

       if self.config_time < os.stat(configfile).st_mtime:
           print "Loading new config from file"
           self.config_time  = os.stat(configfile).st_mtime 
           with open(configfile) as f:
               self.running_config = json.load(f)
       else:
           print "Using cached config"

       if domainname in self.running_config:
           return self.running_config[domainname]
       else:
           return None

