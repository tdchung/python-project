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

    def my_print(self, log_level, *argv):
        time_string = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        if len(argv) is 1:
            if type(argv[0]) is str:
                string = argv[0].replace("\n", "<\\n>").replace("\r", "<\\r>")
            else:
                string = argv[0]
        else:
            string = ""
            for arg in argv:
                string = string + " {}".format(arg)
        mystr = "{} {}: {}".format(time_string, log_level, string)
        print(mystr)

        if self.saveLog is True:
            # if "debug" != self.logLevel and "--DEBUG--" == log_level:
            #     # remove log debug
            #     pass
            # else:
                # pass
                with open(self.logFile, "a+") as myfile:
                    myfile.write("%s\n" % mystr)

    def debug(self, *argv):
        self.my_print("--DEBUG--", *argv)

    def info(self, *argv):
        self.my_print("--INFO--", *argv)

    def error(self, *argv):
        self.my_print("===ERROR===", *argv)

    def warn(self, *argv):
        self.my_print("==WARNING==", *argv)

    def blank(self):
        if self.saveLog is True:
            with open(self.logFile, "a+") as myfile:
                myfile.write("\n")


if __name__ == '__main__':
    # test
    pass
