#!/usr/bin/python
# -*- coding: utf8 -*-

# date:    2017-08-21
# author:  tdchung
# mail:    tdchung.9@gmail.com
#
#           defaultGUI4.py
#
# update
# 2019-04-07          1.0           Create
# 2019-04-21          1.1
#
from __future__ import print_function
import time
import os


class MyPrint:
    def __init__(self, saveLog=False, logFile=u"", logLevel=u"debug"):
        self.saveLog = saveLog
        self.logFile = logFile
        self.logLevel = logLevel
        if self.saveLog is True:
            # self.info("SAVE lOG TO: %s" % self.logFile)
            # with open(self.logFile, "w+") as myfile:
            #     # create a file
            #     pass
            with open(self.logFile, "a+") as myfile:
                myfile.write("\n\nSAVE FILE AT %s\n" %
                             time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))

    def my_print(self, log_level, string):
        if type(string) is not str:
            string = str(string)
        time_string = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        string = string.split("\n")
        for i in range(len(string)):
            # mystr = ("%s -- %s %s: %s" % (os.path.basename(__file__),
            # time_string, log_level, string[i]))
            mystr = ("%s %s: %s" % (time_string, log_level, string[i]))
            print(mystr)
            if self.saveLog is True:
                if "debug" != self.logLevel and "--DEBUG--" == log_level:
                    # remove log debug
                    pass
                else:
                    with open(self.logFile, "a+") as myfile:
                        myfile.write("%s\n" % mystr)

    def debug(self, string):
        self.my_print("--DEBUG--", string)

    def info(self, string):
        self.my_print("--INFO--", string)

    def error(self, string):
        self.my_print("===ERROR===", string)

    def warn(self, string):
        self.my_print("==WARNING==", string)

    def blank(self):
        if self.saveLog is True:
            with open(self.logFile, "a+") as myfile:
                myfile.write("\n")


if __name__ == '__main__':
    # test
    pass
