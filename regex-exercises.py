import re

#Task 1
f = open("regex-matchables.txt", "r")
lines = f.readlines()
f.close()

def get_ip_matches():
    for line in lines:
        if re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", line):
            print(line)

def get_email_matches():
    for line in lines:
        if re.search(r".+@.+\..+", line):
            print(line)

def get_phone_matches():
    for line in lines:
        if re.search(r"(\d){3}-(\d){3}-(\d){4}", line):
            print(line)

def find_users_interactive():
    for line in lines:
        if re.search(r"(.+:){6}.+", line) and re.search(r"sh$", line):
            user = line.split(":")[0]
            print(f"User {user} can log in interactively.")


#get_ip_matches()
#get_email_matches()
#get_phone_matches()
find_users_interactive()