import time

def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(1)


# Create and launch a thread
from threading import Thread

t = Thread(target=countdown, args=(10,))
t.start()
print("Thread is counting")