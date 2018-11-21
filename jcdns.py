#!/usr/bin/env python
import argparse
import config
import os
import sys

"""

    This is the main executable to launch dns daemon

"""

import argparse
from server import Base

def main():
    parser = argparse.ArgumentParser(description='JCDNS')
    parser.add_argument('-f', default='example.json', help='path of zone config')
    parser.add_argument('-d', action='store_true', help='fork and detatch jcdns as daemon')
    args = parser.parse_args()
    config.configfile = args.f

    s = Base()

    if os.getuid() != 0:
        print "Must run as root because DNS binds on port 53"
        sys.exit(1)

    if args.d:
        print "Detaching process..."
        try:
            pid = os.fork()
            if pid > 0:
                print "parent"
                sys.exit(0)
            else:
                print "child"
        except OSError, e:
            print >> sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror)
            sys.exit(1)
           
   
    s.start()

if __name__ == '__main__':
   main()





