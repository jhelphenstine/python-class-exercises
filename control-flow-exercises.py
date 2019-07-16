print("Question1 - Question3")
a = "string"
if (a == "string"):
    print("Successful if test")
elif (a != "string"):
    print("Not equivalent.")
else:
    print("I'm not sure how I got here.")

print("Question4")
for num in range(0,5):
    print(num)

print("Question5")
for num in range(25,42):
    if(num%3 == 0):
        print(num)

print("Question6")
list1 = [36,"thirty six", 5, "fife"]
for x in list1:
    print(x)

print("Question7")
while(1):
    print("This is the loop that never ends")

print("Question8")
x = 0
while (x<5):
    print("String!")
    x+=1

print("Question9")
for x in range(1,16):
    if((x % 2) ==1):
        print(f'192.168.1.{x}')

print("Question10")
a = "Hello World"
for letter in a:
    if (letter == " "):
        break

print("Question11")
for letter in a:
    if(letter == " "):
        continue
    else:
        print(a)

while(1):
    var = input("Input: ")
    if(int(var)==0):
        print("Value is zero")
    if(int(var) != 0):
        if(int(var) > 0):
            print("Value is positive")
        else:
            print("Value is negative")


