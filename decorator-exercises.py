import datetime

#Task 1

'''
def outer(*var):
    outside = "I'm defined in outer()"
    def inside_func():
        nonlocal outside
        print("Inner function now calling string from outer")
        print(outside)
    return inside_func()

outer()
'''

#Task 2

'''
def basic_func(dec_func):
    def to_do_list(*args, **kwargs):
        print("Decorated basic_function with {}".format(dec_func.__name__))
        dec_func(*args, **kwargs)
    return to_do_list

@basic_func
def simple_string():
    print("This is a simple string")

@basic_func
def product(*args):
    x = 1
    for arg in args:
        x *= arg
    print("Product of variables: " + str(x))

simple_string()
product(4,5,6)
'''

#Task 3

def timer_func(dec_func):
    def measure_time(*args, **kwargs):
        start = datetime.datetime.now()
        is_generator = "gen" in dec_func.__name__
        if is_generator:
            for item in dec_func(*args, **kwargs):
                yield item
            end = datetime.datetime.now()
        else:
            dec_func(*args, **kwargs)
            end = datetime.datetime.now()
        total = end - start
        print("It took {0} milliseconds to execute {1}".format(total, dec_func.__name__))
    return measure_time


@timer_func
def large_num_gen(n):
    x,y = 0, 1
    for num in range(n):
        yield x
        x,y = y, x+y

@timer_func
def large_num_func(n):
    x,y = 0,1
    sum = []
    for i in range(n):
        sum.append(x)
        x, y = y, x+y
    return sum


total = 0

for i in large_num_gen(150000):
    total = i

total = 0

for i in large_num_func(150000):
    total = i
#print(total) # Commenting this out because its output is immaterial to this exercise
