from __future__ import print_function
import time
import threading


print_mutex = threading.Lock()


def safe_print(string):
    string = string.splitlines()
    for i in range(len(string)):
        print_mutex.acquire()
        time_string = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        mystr = ("%s: %s" % (time_string, string[i]))
        print(mystr)
        print_mutex.release()
