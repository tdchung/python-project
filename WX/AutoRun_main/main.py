# !/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import sys
import os


# user library
# sys.path.append("common_lib")
# sys.path.append("Login")
# sys.path.append("MainFrame")

# user library
sys.path.append(
    "{}/common_lib".format(os.path.abspath(__file__).replace(os.path.basename(__file__), "")))
sys.path.append(
    "{}/Login".format(os.path.abspath(__file__).replace(os.path.basename(__file__), "")))
sys.path.append(
    "{}/MainFrame".format(os.path.abspath(__file__).replace(os.path.basename(__file__), "")))


# add common lib
# sys.path.append("User_lib")
sys.path.append(
    "{}/User_lib".format(os.path.abspath(__file__).replace(os.path.basename(__file__), "")))

# safe_print("test")
try:
    from MyImages import MyImages
    from lib_myPrint import MyPrint
    from lib_myFireBase import MyFireBase
    from LoginFrame import *
    from MainFrame import *
    from CommonApi import *
except:
    print("Import my print ERROR")


class MyApp(wx.App):

    def OnInit(self):
        '''
        :return:
        '''
        test_list = ['MainFrame/test_script.py']
        main_frame = MainFrame(self, test_list=test_list)
        login_frame = LoginFrame(self, MainApp=main_frame)
        return True
        # login_frame.


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
