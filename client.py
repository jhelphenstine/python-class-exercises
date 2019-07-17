# This is the client. It'll be responsible for:
# -- receiving a connection from the server (i know, i know...)
# The client will prompt the user for command-line input
# - package that up, ship it over to the server
# - receive feedback from the server
# - display the output to the user.
 
import socket # because networking yo
import ipaddress # let's see if I wind up using this or not
import os # for return value
import re # for passphrase
import sys # for exit
import pickle # for transfers
 
def catchSessionStartup(s):
 
    while True:
 
        # The user can control-C, of course
        #print("[*] Beginning listening loop")
        #s.listen() # We now listen in main()
       
        conn, addr = s.accept()
        print(f"[*] Connection from {addr[0]}. Verifying passphrase")
        passphrase = conn.recv(512)
        if re.search("ATDT18005551234", passphrase.decode()):
            print(f"\t[*] Connection from {addr[0]} is valid!")
            conn.sendall("ATA".encode())
            confirmation = conn.recv(512)
            if re.search("CONNECT", confirmation.decode()):
                # Checks are good, moving on.
                pass
            else:
                print("[!] {addr[0]} did not complete the connection!")
                conn = None
        else:
            print(f"\t[!] Connection from {addr[0]} is invalid!")
            print(f"\t[!] Passphrase tendered: {passphrase.decode()}")
            return None
 
        if conn is None:
            print("[!] No valid connection established.")
 
        with conn:
            print("[*] Connection Established.")
            while True:
                command = input("[*] Command: ")
                if command == "ATH":
                   s.close()
                   return 0
                # print(f"I'm sending: {command}") # DEBUG output
                try:
                    conn.sendall(command.encode())
                except OSError as e:
                    print(f"Exception: {e}")
                    s.close() 
                    return -1
                output = conn.recv(1024)
                try:
                    obj = pickle.loads(output)
                except EOFError as e:
                    print("[!] Error - no object received.")
                    #return -1
                print(obj) # This is ugly, but it's good enough for now
            '''
            if obj.stdout:
                print(obj.stdout)
            elif obj.stderr:
                print(obj.stderr)
            '''
 
def main():
    print("Initializing Client")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
	# From the SO question: "How to change tcp keepalive timer using python script"
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
    try:
        s.bind(("0.0.0.0", 31337)) # Tee-hee
        s.listen()
    except OSError as e:
        print("[!] Initializing failed: Could not bind port 31337; is it in use?")
        print(f"OS Error: {e}")
        return 1
 
    # Establish our connection object..and then do everything else, because
    # decomposing this just caused errors.
    results = catchSessionStartup(s)
 
if __name__ == "__main__":
    sys.exit(main())
