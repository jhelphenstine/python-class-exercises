import sys

#Task 1
#print(sys.argv)

#Task 2
if(len(sys.argv) < 4):
    print("[!] Please provide at least 3 arguments.")
    sys.exit
else:
    var2 = sys.argv[2]
    var3 = sys.argv[3]
    var1 = sys.argv[1]

#Task3: When using the sys.stdin.read, I have to specify how many characters to read
var4 = sys.stdin.read(5)
print(var4)

