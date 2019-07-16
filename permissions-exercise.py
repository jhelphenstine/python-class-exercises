import ctypes, os
#print(os.listdir("C:\\"))

#print(os.getlogin())
try:
 is_admin = os.getuid() == 0
except AttributeError:
 is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

if(not is_admin):
    print("You....shall....not....pass!")

os.system("ping -n 4 192.168.1.1")

if(is_admin):
    print("On a UNIX system, I'd be reading from, and printing the contents of, /etc/shadow")