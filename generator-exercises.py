def exp_generator():
    x = 2
    for num in range(1,10):
        yield x
        x = x**num

total = 0
for i in exp_generator():
    total = i
print(i)