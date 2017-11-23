#!/usr/bin/env python
import socket
import itertools
import subprocess
import sys
import os
from datetime import datetime

subprocess.call('clear', shell=True)

def ip_range(input_string):
    octets = input_string.split('.')
    chunks = [map(int, octet.split('-')) for octet in octets]
    ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]

    for address in itertools.product(*ranges):
        yield '.'.join(map(str, address))

def scanIP(remoteServerIP, remotePorts):
    print "-" * 60
    print "Please wait, scanning remote host", remoteServerIP
    print "-" * 60
    t1 = datetime.now()
    try:
        response = os.system("ping -c 1 " + remoteServerIP + " > /dev/null 2>&1")
        if response == 0:
            print "=" * 60
            print remoteServerIP, 'is up!'
        else:
            print remoteServerIP, 'is down or ICMP is not allowed!'
        
        for port in remotePorts:  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(.001) 
            result = sock.connect_ex((remoteServerIP, int(port)))
            if result == 0:
                print "Port {}: 	 Open".format(port)
            sock.close()
        if response == 0:
            print "=" * 60

    except KeyboardInterrupt:
        print "You pressed Ctrl+C"
        sys.exit()

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        sys.exit()

    except socket.error:
        print "Couldn't connect to server"
        sys.exit()

    t2 = datetime.now()
    total =  t2 - t1
    print 'Scanning Completed in: ', total

remoteServer       = raw_input("Enter a remote VLAN to scan (eg:192.168.1-255.1-255): ")
remotePortsStr     = raw_input("Enter a remote VLAN to scan (eg:21,22,23,64,80,443,81,3000,3306,5432,8000,8080,8888) or (*): ")

if len(remotePortsStr) == 0:
    remotePortsStr = '21,22,23,64,80,443,81,3000,3306,5432,8000,8080,8888'

for ip in ip_range(remoteServer):
    if remotePortsStr== "*":
        remotePorts = range(1,65535)
    else:
        remotePorts = remotePortsStr.split(",") 
    scanIP(socket.gethostbyname(ip),remotePorts)
