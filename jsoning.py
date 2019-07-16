#! /usr/bin/env python
import json
Object = ["eggs", "SPAM", "toast", None, 3, 1.6]
### Using the json module create a json object that is not written to a file.
### Then print the json object to compare the values with the original object
j = json.dumps(Object)
###############################################
### Load the json object you created as a new object and print that object to ensure that it contains the same values as Object
k = json.loads(j)
print(Object)
print(k)
###############################################
### Create a json file that serializes all the objects in the script
### Open the .json file in a text viewer or editor
f = open("jsons.txt", "w")
for obj in [Object, k]:
    json.dump(obj, f)
f.close()
###############################################