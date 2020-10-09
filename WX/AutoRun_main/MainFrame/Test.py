#!/usr/bin/env python
# _*_ coding: utf-8 _*_


import os
import sys
import wx
import time

from datetime import datetime
import threading
import random

from CommonApi import *

# user library
# sys.path.append("../User_lib")
sys.path.append("{}/../User_lib".format(os.path.abspath(__file__).
                                        replace(os.path.basename(__file__), "")))


# demo log
# path = os.path.abspath(__file__).replace(__file__, "")
path = "{}/../logs/".format(os.path.abspath(
    __file__).replace(os.path.basename(__file__), ""))
log_path = "{}/logs/".format(path)


# redirect
class GuiOnlyOutput:
    def __init__(self, gui_out, log_path=log_path, log_name="log"):
        self.gui_out = gui_out
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self.log_file = "%s/%s.txt" % (log_path, log_name)
        filetimestamp = time.strftime("__%Y_%m_%d__%H_%M_%S", time.localtime())
        self.log_file_timestamp = "%s/%s%s.txt" % (
            log_path, log_name, filetimestamp)

    def write(self, text):
        # TODO: add mutex or semaphore
        # self.gui_out.SetDefaultStyle(wx.TextAttr("blue"))
        # self.gui_out.AppendText(text)
        # self.gui_out.flush()
        # self.gui_out.SetDefaultStyle(wx.TextAttr("black"))
        # self.gui_out.write(text)

        # self.gui_out.SetDefaultStyle(wx.TextAttr(wx.Colour(random.randint(0, 255),
        #                                                    random.randint(0, 255),
        #                                                    random.randint(0, 255))))
        self.gui_out.SetDefaultStyle(wx.TextAttr(wx.Colour(100, 22, 100)))
        self.gui_out.AppendText(text)
        # self.gui_out.flush()
        with open(self.log_file, 'a') as f:
            # self.gui_out.AppendText(self.log_file)
            f.write(text)
        with open(self.log_file_timestamp, 'a') as f:
            f.write(text)


class NoneRedirect:
    def __init__(self, out):
        self.out = out

    def write(self, text):
        # self.gui_out.SetDefaultStyle(wx.TextAttr("blue"))
        # self.gui_out.AppendText(text)
        self.out.write(text)
        # self.gui_out.SetDefaultStyle(wx.TextAttr("black"))


pause = False
PauseLock = threading.Lock()
kill = False
displayTrace = False


class Thread(threading.Thread):
    """Sous-classe de threading.Thread, avec une methode stop() et pause()"""

    def __init__(self, *args, **keywords):
        global kill
        threading.Thread.__init__(self, *args, **keywords)

        kill = False
        self.__kill = False
        self.__pause = False
        self.__PauseLock = threading.Lock()  # Lock to break the excecution
        self.__EndOfThreadEvent = threading.Event()  # Event to detect the end of Thread

    def start(self):
        self.__EndOfThreadEvent.clear()  # Reset Event to detect the end of Thread
        self.run_sav = self.run
        self.run = self.run2
        threading.Thread.start(self)

    def Pause(self):
        self.__pause = True
        self.__PauseLock.acquire()

    def Continue(self):
        if self.__pause:
            self.__pause = False
            self.__PauseLock.release()

    def stop(self):
        if self.__pause:
            self.__PauseLock.release()
            self.__pause = False
        self.__kill = True

    def run2(self):
        sys.settrace(self.__trace)
        self.run_sav()
        self.run = self.run_sav
        self.__EndOfThreadEvent.set()  # Set Event to detect the end of Thread

    def __trace(self, frame, event, arg):
        global pause, PauseLock, kill, displayTrace
        if self.__kill or kill:  # Test if stop is require
            if event == 'line':
                raise SystemExit()
        if pause and event == 'line':  # Test if global pause is require
            # print "global pause"
            PauseLock.acquire()
            PauseLock.release()
        if self.__pause and event == 'line':  # Test if pause is require
            # print "local pause"
            self.__PauseLock.acquire()
            self.__PauseLock.release()
        return self.__trace

    def DisplayTrace(self, state):
        global displayTrace
        displayTrace = state

    def GetPauseStatus(self):
        return self.__pause

    def WaitEndOfThread(self, timeout=None):  # timeout in milliseconds
        try:
            if timeout != None:
                start = datetime.now
                self.__EndOfThreadEvent.wait(timeout / 1000.0)
                diff = datetime.now - start
                diff_time = diff.seconds + diff.microseconds / 1000000.0
                self.__EndOfThreadEvent.clear()
                return diff_time < timeout
            else:
                self.__EndOfThreadEvent.wait()
                self.__EndOfThreadEvent.clear()
                return True
        except SystemExit:
            self.__kill = True
            raise SystemExit()


class Test(Thread):
    "this class instanciates threads ; it shall be instanciated using start() and not run()"
    "run method will be executed automatically by Python"

    def __init__(self, list_test, test_output, is_gui=True):
        '''
        initial
        :param list_test:
        :param test_output:
        '''
        Thread.__init__(self)
        self.list_test = list_test
        self.test_output = test_output
        self.is_gui = is_gui
        self.saveStreams = None

    def run(self):
        "this method executes the tests cases the one after the others"
        "when instancating the thread, it is advised to use start() and not directly run()"
        try:
            # TODO: remove, debug redirect
            # print("==================")
            list_test = self.list_test

            # redirect
            if self.is_gui:
                self.saveStreams = sys.stdout, sys.stderr
                gui_out = self.test_output
                test_output = GuiOnlyOutput(gui_out)
                sys.stdout = test_output
                sys.stderr = sys.stdout
            else:
                self.saveStreams = sys.stdout, sys.stderr
                test_output = NoneRedirect(sys.stdout)
                sys.stdout = test_output
                sys.stderr = sys.stdout

            for test in list_test:
                # print(test)
                try:
                    # python 2
                    # execfile(test)
                    exec(open(test).read())
                except Exception as e:
                    print(e)
        except SystemExit:
            # print("STOP button")
            # print(e)
            raise
            pass
        finally:
            # return
            sys.stdout, sys.stderr = self.saveStreams
            pass


if __name__ == '__main__':
    test = Test(["test_script.py"], sys.stdout, is_gui=False)
    test.start()
    time.sleep(2)
    test.Pause()
    time.sleep(10)
    test.Continue()
