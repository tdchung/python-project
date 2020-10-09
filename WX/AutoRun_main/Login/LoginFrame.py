#!/usr/bin/python
# -*- coding: utf8 -*-

# date:    2019-XX-XX
# author:  tdchung
# mail:    tdchung.9@gmail.com
#
# update
# 2019-11-06          1.0           Create
#
#
from __future__ import print_function
import wx
import platform
import io
import hashlib
import sys
import re
import os

# user library
# sys.path.append("../common_lib")
sys.path.append("{}/../common_lib".format(os.path.abspath(__file__).
                                          replace(os.path.basename(__file__), "")))


# define config
sys.path.append("{}/../Config".format(os.path.abspath(__file__).
                                      replace(os.path.basename(__file__), "")))

try:
    from lib_myFireBase import MyFireBase
    from lib_myPrint import MyPrint
    from MyImages import MyImages
except:
    print("Import my print ERROR")

try:
    # from config import *
    # TODO: the filebase token is in the config file
    MY_FIREBASE = "base64data"
    if MY_FIREBASE is None:
        raise Exception
except Exception:
    raise Exception


# define class
MyImages = MyImages()
myPrint = MyPrint()
myFireBase = MyFireBase(MY_FIREBASE, True)


version = '1.0'

# define most valif email
email_re = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class LoginFrame(wx.Frame):
    # Linux: Linux
    # Mac: Darwin
    # Windows: Windows
    default_size = wx.Size(360, 240)
    if platform.system() in ["Linux", "Darwin"]:
        default_size = wx.Size(360, 220)

    def __init__(self, parent, title='Login Form', MainApp=None):
        # super(LoginFrame, self).__init__(parent, title=title, size=self.default_size)
        wx.Frame.__init__(self, None, title=title, size=self.default_size)

        self.MainApp = MainApp
        myPrint.debug(MainApp)
        myPrint.debug(self.MainApp)
        myPrint.debug(parent)
        self.parent = parent
        # define
        self._isUser = False
        self._isPassword = False

        self._user = ""
        self._password = ""
        self._confirm_password = ""
        self._email = ""

        self._isPasswordShow = False
        self._isCreateAccount = False

        self.isAdmin = False

        # set icon for application
        try:
            icon = wx.Icon()
            # self.images = MyImages()
            data = MyImages.getIconApp()
            bytes_stream = io.BytesIO(data)
            image = wx.Image(bytes_stream)
            icon.CopyFromBitmap(wx.Bitmap(image))
            self.SetIcon(icon)

        except Exception as e:
            myPrint.debug(e)
            pass
        # self.SetBackgroundColour('blue')
        # set minimum size
        # self.SetSizeHints(self.default_size, wx.DefaultSize)
        self.SetMaxSize(self.default_size)
        self.SetMinSize(self.default_size)

        self.login_panel_init()
        self.Centre()
        self.Show()

        self.Bind(wx.EVT_CLOSE, self._when_closed)

    def login_panel_init(self):

        self.login_panel = wx.Panel(self)

        # font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        # font = wx.Font(pointSize=12, family=wx.FONTFAMILY_SCRIPT, style=wx.FONTSTYLE_SLANT,
        # weight=wx.FONTWEIGHT_BOLD)
        font = wx.Font(pointSize=12, family=wx.FONTFAMILY_SCRIPT, style=wx.FONTSTYLE_NORMAL,
                       weight=wx.FONTWEIGHT_BOLD)
        # btnfont = wx.Font(pixelSize = 10, wx.MODERN, wx.NORMAL, wx.BOLD)
        # toofont = wx.Font(pixelSize = 9, wx.MODERN, wx.SLANT , wx.BOLD)

        self.vbox_main = wx.BoxSizer(wx.VERTICAL)

        self.vbox_main.Add(wx.StaticLine(self.login_panel),
                           0, wx.ALL | wx.EXPAND, 0)

        # USER
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sText1 = wx.StaticText(
            self.login_panel, label='User name:', size=(80, 20))
        # self.sText1.SetFont(font)
        self.tCtrl_user = wx.TextCtrl(self.login_panel)
        # self.btn_password = wx.Button(self.login_panel, label='..', size=(40, 23))
        fgs = wx.FlexGridSizer(1, 2, 0, 0)
        # fgs = wx.FlexGridSizer(1, 3, 0, 0)
        fgs.AddMany([(self.sText1, 1, wx.ALIGN_BOTTOM),
                     (self.tCtrl_user, 1, wx.EXPAND)])
        fgs.AddGrowableCol(1, 1)
        hbox1.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=2)
        self.vbox_main.Add(hbox1, flag=wx.EXPAND | wx.LEFT |
                           wx.RIGHT | wx.TOP, border=2)
        self.vbox_main.Add((-1, 5))

        # PASSWORD
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sText2 = wx.StaticText(
            self.login_panel, label='Password:', size=(80, 20))
        # self.sText2.SetFont(font)
        self._password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.tCtrl_password = wx.TextCtrl(self.login_panel, style=wx.TE_PASSWORD |
                                          wx.TE_PROCESS_ENTER)
        self.tCtrl_password_show = wx.TextCtrl(
            self.login_panel, style=wx.TE_PROCESS_ENTER)
        self.tCtrl_password_show.Hide()
        self._password_sizer.AddMany([(self.tCtrl_password, 1, wx.EXPAND),
                                      (self.tCtrl_password_show, 1, wx.EXPAND)])
        self.btn_password = wx.Button(
            self.login_panel, label='..', size=(30, 20))
        # fgs2 = wx.FlexGridSizer(1, 2, 0, 0)  # FlexGridSizer(rows, cols, vgap, hgap)
        # FlexGridSizer(rows, cols, vgap, hgap)
        fgs2 = wx.FlexGridSizer(1, 3, 0, 0)
        fgs2.AddMany([(self.sText2, 1, wx.ALIGN_BOTTOM),
                      (self._password_sizer, 1, wx.EXPAND),
                      (self.btn_password, 1, wx.EXPAND)])
        # Specifies that column idx (starting from zero) should be grown
        fgs2.AddGrowableCol(1, 1)
        # if there is extra space available to the sizer.
        hbox2.Add(fgs2, proportion=1, flag=wx.ALL | wx.EXPAND, border=2)
        self.vbox_main.Add(hbox2, flag=wx.EXPAND | wx.LEFT |
                           wx.RIGHT | wx.TOP, border=2)
        # self.vbox_main.Add((-1, 5))

        # CONFIRM PASSWORD
        self.hbox_pass_confirm = wx.BoxSizer(wx.HORIZONTAL)
        self.sText_pass_cf = wx.StaticText(
            self.login_panel, label='Confirm:', size=(80, 20))
        # self.sText2.SetFont(font)
        self.tctrl_pass_cf = wx.TextCtrl(
            self.login_panel, style=wx.TE_PASSWORD)
        self.sText_pass_cf.Hide()
        self.tctrl_pass_cf.Hide()
        # FlexGridSizer(rows, cols, vgap, hgap)
        self.fgs_pass_cf = wx.FlexGridSizer(1, 2, 0, 0)
        self.fgs_pass_cf.AddMany([(self.sText_pass_cf, 1, wx.ALIGN_BOTTOM),
                                  (self.tctrl_pass_cf, 1, wx.EXPAND)])
        # Specifies that column idx (starting from zero)
        self.fgs_pass_cf.AddGrowableCol(1, 1)
        # should be grown
        # if there is extra space available to the sizer.
        self.hbox_pass_confirm.Add(self.fgs_pass_cf, proportion=1,
                                   flag=wx.ALL | wx.EXPAND, border=2)
        # self.hbox_pass_confirm.Hide(self.fgs_pass_cf)
        self.vbox_main.Add(self.hbox_pass_confirm,
                           flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2)
        # Hide this field
        # self.vbox_main.Hide(self.hbox_pass_confirm)
        # self.vbox_main.Add((-1, 5))

        # EMAIL
        self.hbox_email = wx.BoxSizer(wx.HORIZONTAL)
        self.sText_email = wx.StaticText(
            self.login_panel, label='Email:', size=(80, 20))
        # self.sText2.SetFont(font)
        self.tctrl_email = wx.TextCtrl(self.login_panel)
        self.sText_email.Hide()
        self.tctrl_email.Hide()
        # FlexGridSizer(rows, cols, vgap, hgap)
        self.fgs_email = wx.FlexGridSizer(1, 2, 0, 0)
        self.fgs_email.AddMany([(self.sText_email, 1, wx.ALIGN_BOTTOM),
                                (self.tctrl_email, 1, wx.EXPAND)])
        # Specifies that column idx (starting from zero)
        self.fgs_email.AddGrowableCol(1, 1)
        # should be grown
        # if there is extra space available to the sizer.
        self.hbox_email.Add(self.fgs_email, proportion=1,
                            flag=wx.ALL | wx.EXPAND, border=2)
        self.vbox_main.Add(self.hbox_email, flag=wx.EXPAND |
                           wx.LEFT | wx.RIGHT | wx.TOP, border=2)

        # REMEMBER PASSWORD
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.sText4_empty = wx.StaticText(
            self.login_panel, label='', size=(80, 20))
        self.checkbox4 = wx.CheckBox(
            self.login_panel, label='Remember my password')
        self.checkbox4.Show()
        # self.sText4.SetFont(font)
        # self.tCtrl4 = wx.TextCtrl(self.login_panel)
        fgs4 = wx.FlexGridSizer(1, 2, 0, 0)
        fgs4.Add(self.sText4_empty, 0, wx.ALIGN_BOTTOM)
        fgs4.Add(self.checkbox4, 0, wx.EXPAND)
        # fgs4.AddMany([(self.sText4, 1, wx.ALIGN_BOTTOM), (self.tCtrl4, 1, wx.EXPAND)])
        fgs4.AddGrowableCol(1, 1)
        hbox4.Add(fgs4, proportion=1, flag=wx.ALL | wx.EXPAND, border=2)
        self.vbox_main.Add(hbox4, flag=wx.EXPAND | wx.LEFT |
                           wx.RIGHT | wx.TOP, border=2)
        self.vbox_main.Add((-1, 5))

        # BUTTONS
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn2 = wx.Button(self.login_panel, label='LOGIN', size=(140, 30))
        self.btn2.Disable()
        self.btn3 = wx.Button(
            self.login_panel, label='SIGN UP', size=(140, 30))
        self.sText6_empty = wx.StaticText(
            self.login_panel, label='', size=(80, 20))
        # gs = wx.GridSizer(1, 3, 5, 5) # 1 x 3
        # FlexGridSizer(rows, cols, vgap, hgap)
        fgs6 = wx.FlexGridSizer(1, 3, 0, 0)
        fgs6.Add(self.sText6_empty, 0, wx.ALIGN_BOTTOM)
        fgs6.Add(self.btn2, 0, wx.EXPAND)
        fgs6.Add(self.btn3, 0, wx.EXPAND)
        # fgs6.AddMany([(self.sText6_empty, 1, wx.ALIGN_BOTTOM),
        # (self.btn2, 1, wx.EXPAND), (self.btn3, 1, wx.EXPAND)])
        hbox6.Add(fgs6, proportion=1, flag=wx.ALL | wx.EXPAND, border=2)
        # self.vbox_main.Add(hbox6,
        #                    flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_BOTTOM, border=2)
        self.vbox_main.Add(hbox6,
                           flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2)
        self.vbox_main.Add((-1, 5))

        # STATIC LINE
        self.vbox_main.Add(wx.StaticLine(self.login_panel, -1, style=wx.LI_HORIZONTAL,
                                         size=(10, -1)), 0, wx.EXPAND | wx.ALL, border=2)

        # INFO
        self.text_info = wx.StaticText(
            self.login_panel, label='', size=(200, 20))
        self.vbox_main.Add(self.text_info, 0, wx.EXPAND | wx.ALL, border=2)

        # HELP
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        self.sText_help = wx.StaticText(self.login_panel, label='Need help to sign in?',
                                        size=(-1, -1), style=wx.ALIGN_RIGHT)
        self.btn_help = wx.Button(
            self.login_panel, label="I CAN'T SIGN IN...", size=(250, 30))
        # fgs7 = wx.FlexGridSizer(1, 2, 0, 0)
        fgs7 = wx.GridSizer(1, 2, 0, 0)
        fgs7.Add(self.sText_help, 1, wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL)
        fgs7.Add(self.btn_help, 1, wx.EXPAND)
        # fgs7.AddMany([(self.tCtrl7, 1, wx.EXPAND)])
        hbox7.Add(fgs7, proportion=1, flag=wx.ALL | wx.EXPAND, border=2)

        self.vbox_main.Add(hbox7, flag=wx.EXPAND | wx.LEFT |
                           wx.RIGHT | wx.TOP, border=2)
        self.vbox_main.Add((-1, 5))

        self.login_panel.SetSizer(self.vbox_main)
        self.Layout()

        # self.Bind(wx.EVT_BUTTON, self.btn1_event, self.btn1)
        # set bind for button
        self.Bind(wx.EVT_BUTTON, self.btn_password_event, self.btn_password)
        self.Bind(wx.EVT_BUTTON, self.btn2_event, self.btn2)
        self.Bind(wx.EVT_BUTTON, self.btn3_event, self.btn3)
        self.Bind(wx.EVT_BUTTON, self.btn_help_event, self.btn_help)

        # set bind for text control
        self.Bind(wx.EVT_TEXT, self.tctrl_user_event, self.tCtrl_user)
        self.Bind(wx.EVT_TEXT, self.tctrl_password_event, self.tCtrl_password)
        self.Bind(wx.EVT_TEXT, self.tctrl_password_show_event,
                  self.tCtrl_password_show)
        self.Bind(wx.EVT_TEXT, self.tctrl_pass_cf_event, self.tctrl_pass_cf)
        self.Bind(wx.EVT_TEXT, self.tctrl_email_event, self.tctrl_email)

        # TODO: non enter is handled
        # enter handler
        self.Bind(wx.EVT_TEXT_ENTER, self.btn2_event, self.tCtrl_password)
        self.Bind(wx.EVT_TEXT_ENTER, self.btn2_event, self.tCtrl_password_show)

        # Checkbox event
        self.Bind(wx.EVT_CHECKBOX, self.checkbox4_event, self.checkbox4)

    def checkbox4_event(self, evt):
        myPrint.debug("DEBUG: check box: %s" % str(self.checkbox4.GetValue()))

    def tctrl_user_event(self, evt):
        # self._isUser = True
        self._enable_button()

    def tctrl_password_event(self, evt):
        # self.btn2.Enable()
        self._enable_button()
        # self.btn2.SetFocus()

    def tctrl_password_show_event(self, evt):
        # self.btn2.Enable()
        self._enable_button()
        # self.btn2.SetFocus()

    def tctrl_pass_cf_event(self, evt):
        # self.btn2.Enable()
        self._enable_button()

    def tctrl_email_event(self, evt):
        # self.btn2.Enable()
        self._enable_button()

    # def btn1_event(self, evt):
    #     dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
    #     if dlg.ShowModal() == wx.ID_OK:
    #         myPrint.debug("You chose %s" % dlg.GetPath())
    #         self.tCtrl1.Clear()
    #         self.tCtrl7.Clear()
    #         self.tCtrl1.WriteText(str(dlg.GetPath()))
    #         pass
    #     dlg.Destroy()

    def btn_password_event(self, evt):
        self.text_info.SetLabel("")
        myPrint.debug("DEBUG: btn_password_event")
        if self._isCreateAccount:
            return
        myPrint.debug("DEBUG: %s" % str(self.GetSize()))
        # Toggle password
        self.tCtrl_password.Show(self._isPasswordShow)
        self.tCtrl_password_show.Show(not self._isPasswordShow)

        if not self._isPasswordShow:
            self.tCtrl_password_show.SetValue(self.tCtrl_password.GetValue())
            self.tCtrl_password_show.SetFocus()
        else:
            self.tCtrl_password.SetValue(self.tCtrl_password_show.GetValue())
            self.tCtrl_password.SetFocus()
        self.tCtrl_password.GetParent().Layout()
        self._isPasswordShow = not self._isPasswordShow

        # self._update_FrameSize(self.GetSize() + (0, 50))
        # self.vbox_main.Show(self.hbox_pass_confirm)
        # myPrint.debug(self.GetSize())
        # myPrint.debug(self.SetSize(wx.Size(360, 300)))

    def btn2_event(self, evt):
        self.text_info.SetLabel("")
        self.btn2.Disable()
        # import time
        # time.sleep(2)
        # in case LOGIN
        if not self._isCreateAccount:
            self._user = self.tCtrl_user.GetValue()
            self._password = self.tCtrl_password.GetValue() \
                if not self._isPasswordShow                 \
                else self.tCtrl_password_show.GetValue()
            # myPrint.debug("DEBUG: login, user: %s, pw: %s" %(self._user, self._password))
            myPrint.debug("DEBUG: login, user: %s, pw: %s"
                          % (hashlib.sha256(self._user.lower().encode()).hexdigest(),
                             hashlib.sha256(self._password.encode()).hexdigest()))
            rsp = myFireBase.validateUser(self._user.lower(), self._password)
            if rsp == 1:
                self.text_info.SetLabel("User or password correct")
                myPrint.debug("DEBUG: login passed")
                # Internal: check if Admin
                if "admin" == self._user.lower():
                    myPrint.debug("DEBUG: In permission create new account")
                    self.isAdmin = True
                # TODO: destroy and go to you app
                else:
                    self.Destroy()
                    self.MainApp.Show()

            elif rsp == 0:
                self.text_info.SetLabel("Password is incorrect")
                myPrint.debug("DEBUG: login failed, Password is incorrect")
            elif rsp == -1:
                self.text_info.SetLabel("User is not existed")
                myPrint.debug("DEBUG: login failed, User is not existed")
            else:
                self.text_info.SetLabel(
                    "Something wrong, check your connection")
                myPrint.debug("DEBUG: login failed, Exception")
            #     self.text_info.SetLabel("User or password incorrect")
            #     myPrint.debug("DEBUG: login failed")
            # else:
            #     myPrint.debug("DEBUG: login Passed")

        # in case create new Account
        else:
            self._user = self.tCtrl_user.GetValue()
            self._password = self.tCtrl_password.GetValue() \
                if not self._isPasswordShow \
                else self.tCtrl_password_show.GetValue()
            self._confirm_password = self.tctrl_pass_cf.GetValue()
            self._email = self.tctrl_email.GetValue()
            myPrint.debug("DEBUG: CREATE, user: %s, pw: %s, cf: %s, email: %s" %
                          (self._user, self._password, self._confirm_password, self._email))
            # 1. Check is user existed
            if myFireBase.isUserExisted(self._user.lower()):
                myPrint.debug("DEBUG: User is already existed")
                self.text_info.SetLabel("")
                self.text_info.SetLabel("User is already existed")
                self.tCtrl_user.SetFocus()
                self.tCtrl_user.GetParent().Layout()
                return
            # 2. Check confirm password
            if self._password != self._confirm_password:
                myPrint.debug("DEBUG: password confirm not match")
                self.text_info.SetLabel("")
                self.text_info.SetLabel("Password confirm not match")
                self.tctrl_pass_cf.SetFocus()
                self.tctrl_pass_cf.GetParent().Layout()
                return
            # 3. check email is correct format
            if re.match(email_re, self._email) is not None:
                myPrint.debug("DEBUG: email format is correct")
            else:
                myPrint.debug("DEBUG: email is invalid")
                self.text_info.SetLabel("Please enter correct email")
                self.tctrl_email.SetFocus()
                self.tctrl_email.GetParent().Layout()
                return
            # 4. create aucount
            if not self.isAdmin:
                self.text_info.SetLabel("")
                self.text_info.SetLabel(
                    "Contact to tdchung to create new account")
            else:
                if myFireBase.createNewAccount(self._user.lower(), self._password, self._email):
                    myPrint.debug("Account is created")
                    self.text_info.SetLabel("")
                    self.text_info.SetLabel("Account is created")
                    self.btn3.SetLabel("SIGN IN")
                    self.btn3.GetParent().Layout()
                else:
                    myPrint.debug("Something go wrong ...")
                # set to Failed. Only 1 Account is create for 1 admin session
                self.isAdmin = False
        self.btn2.Enable()
        return

    def btn3_event(self, evt):
        self.text_info.SetLabel("")
        self.sText_pass_cf.Show(not self._isCreateAccount)
        self.tctrl_pass_cf.Show(not self._isCreateAccount)
        self.tctrl_email.Show(not self._isCreateAccount)
        self.sText_email.Show(not self._isCreateAccount)
        if not self._isCreateAccount:
            self._isPasswordShow = False
            self.tCtrl_password.Show(not self._isPasswordShow)
            self.tCtrl_password_show.Show(self._isPasswordShow)
        # clear value
        self.tctrl_email.SetValue("")
        self.tCtrl_password.SetValue("")
        self.tCtrl_password_show.SetValue("")
        self.tctrl_pass_cf.SetValue("")
        self.checkbox4.Show(self._isCreateAccount)
        self.sText4_empty.Show(self._isCreateAccount)
        self._isCreateAccount = not self._isCreateAccount
        self._update_FrameSize((self.GetSize() + (0, 40)) if self._isCreateAccount
                               else (self.GetSize() - (0, 40)))
        self.btn3.SetLabel("CANCEL" if self._isCreateAccount else "SIGN UP")
        self.btn2.SetLabel("CREATE" if self._isCreateAccount else "LOGIN")
        self.SetTitle(
            "Create new account.." if self._isCreateAccount else "Login form")
        self.tctrl_pass_cf.GetParent().Layout()
        myPrint.debug("DEBUG: self._isCreateAccount: %s" %
                      str(self._isCreateAccount))

        # self.btn2.Enable()
        # self.Destroy()
        pass

    def btn_help_event(self, evt):
        myPrint.debug("DEBUG: help zxczvcbcvb")

    def _when_closed(self, evt):
        # myPrint.debug("close here")
        self.Destroy()
        self.MainApp.Destroy()

    # ----------------------------------------------------------------------------------------------
    # private functions
    # ----------------------------------------------------------------------------------------------

    def _update_FrameSize(self, size):
        # if self.GetSize() > size:
        myPrint.debug("_update_FrameSize")
        x1, y1 = size
        x2, y2 = self.GetSize()
        if y1 > y2:
            self.SetMaxSize(size)
            self.SetMinSize(size)
        else:
            self.SetMinSize(size)
            self.SetMaxSize(size)
        self.SetSize(size)

    def _enable_button(self):
        self.text_info.SetLabel("")
        """
        check if we should enable login button
        """
        # LOGIN form
        if not self._isCreateAccount:
            if self.tCtrl_user.GetValue() != "" and          \
                    (self.tCtrl_password.GetValue() if not self._isPasswordShow else
                     self.tCtrl_password_show.GetValue()) != "":
                self.btn2.Enable()
            else:
                self.btn2.Disable()
        # CREATE form
        else:
            if self.tCtrl_user.GetValue() != "" and          \
                    self.tCtrl_password.GetValue() != "" and \
                    self.tctrl_pass_cf.GetValue() != "" and  \
                    self.tctrl_email.GetValue() != "":
                self.btn2.Enable()
            else:
                self.btn2.Disable()

    # ----------------------------------------------------------------------------------------------
    # delete
    # ----------------------------------------------------------------------------------------------
    def __del__(self):
        pass


if __name__ == '__main__':
    app = wx.App()
    LoginFrame(None)
    app.MainLoop()
