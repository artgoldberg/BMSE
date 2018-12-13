from time import sleep

def power_of_2(n):
    return n > 0 and (n & (n - 1)) == 0

'''
for i in range(30):
    if power_of_2(i):
        print(i)
'''

count = 0
while True:
    sleep(1)
    count += 1 
    if power_of_2(count):
        print('.', end="", flush=True)



