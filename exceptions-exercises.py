#Task0 -- Exception POC
'''
try :
    print("This is my" + failedVar + " format string")
except NameError:
    print("Ha-ha. You fail again!")
finally:
    print("In C there is only do{} or do{}while(!); there is no try:")
'''
#Task1
bad_list = ['this','that','and','the','other',2]
'''
try:
    for bad in bad_list:
	    print(bad * bad)

    while len(bad_list) > 0:
	    print('bad_list is popping')
	    print(bad_list.pop(0))
except Exception as e:
    print("That's just not going to work for me.")
    print(f"Exception: {e}")
'''
#Task2
'''
string1='this is my string for task '
string2=2

def concat(string1,string2):
    if len(str(string1)) >= 0:
        try:
            print(string1 + string2)
        except TypeError as e:
            print("You can't concatenate those things!")
            print(f"Exception: {e}")

concat(string1,string2)
'''

#Task3
# The objective of this code is to perform basic arithmetic on g0 through g3
# The errors must be handled individually and there must be execpt
# statements to account for errors that can be caused by user inputs

def lets_do_maths():
    g0 = input('What would you like to enter for the value of g0? ')
    g1 = '4'
    g2 = 5
    g3 = None
    try:
        g4 = g0 + g1
        g5 = g2 * g0
        g6 = g3 + g4
    except TypeError as e:
        print("You can't evaluate None for arithmetic")
        print(f"Exception: {e}")
    try:
        result = g4+g5%g6
    except UnboundLocalError as e:
        print("You can't use g6, because it's undefined, because g3+ g4 threw an exception")
        print(f"Exception: {e}")
    try:
        return result
    except UnboundLocalError as e:
        print("You can't return 'result', because it's undefined, because of prior exceptions")
        print(f"Exception: {e}")
        return "Error: Function failed to execute correctly; no results produced."


x = lets_do_maths()
print(x)