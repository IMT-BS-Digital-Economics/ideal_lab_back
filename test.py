from time import sleep

from os import getpid

print(getpid())

for i in range(0, 1000):
    print(f'Hello: {i}')
    sleep(100)
