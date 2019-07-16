import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",4455))
s.sendto("This is a string of text. It's not going to be full of numbers, and probably won't hit 512 bytes, though I could possibly generate a range of numbers and send them...".encode(), ("127.0.0.1",4455))
