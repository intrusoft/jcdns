#!/usr/bin/env python

"""

    This is the main executable to launch dns daemon

"""


from server import Base

def main():
    s = Base()
    s.start()

if __name__ == '__main__':
   main()





