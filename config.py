""" Read from the zone config file """

import json
import os

configfile = 'example.json'

class Config:
   def __init__(self):
       self.running_config = None
       self.config_time = 0

   def getconfig(self, domainname):
       """ Search the config for a specific domain name """

       # check if time we last read file is older than files actual modification time
       if self.config_time < os.stat(configfile).st_mtime:
           self.config_time  = os.stat(configfile).st_mtime 
           print "Reading config from file system at %s " % configfile
           with open(configfile) as f:
               self.running_config = json.load(f)
       else:
           print "Reading config from cache"

       if domainname in self.running_config:
           return self.running_config[domainname]
       else:
           return None

