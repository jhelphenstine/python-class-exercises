import sys

if(len(sys.argv) > 1):
    print(sys.argv[1])
else:
    var1 = sys.stdin.read(20)
    print(var1)