import _thread
import time

def testThread():
    while (1):
        print("hello from thread")
        time.sleep(2)

def testThread1():
    while (1):
        print("hello from thread111111")
        time.sleep(0.5)

_thread.start_new_thread(testThread())
_thread.start_new_thread(testThread1())
