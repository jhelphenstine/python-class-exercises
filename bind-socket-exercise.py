import ipaddress
import socket

ip = ipaddress.ip_address("8.8.8.8")

net = ipaddress.ip_network("192.168.100.0/24")

ipInterface = ipaddress.ip_interface("192.168.100.2")

mask = net.netmask

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0",4455))
s.listen(1)
c, addr = s.accept()
print(f"Connection from {addr[0]} at port {addr[1]}")
caught = c.recv(512)
print(caught)