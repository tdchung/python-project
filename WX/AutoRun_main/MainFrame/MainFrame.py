# !/usr/bin/python
# -*- coding: utf8 -*-

# date:    2019-08-21
# author:  tdchung
# mail:    tdchung.9@gmail.com
#
# update
# 2019-xx-xx
#
#

from __future__ import print_function

import wx
import sys
import io
import subprocess
import time
import os

# user library
# sys.path.append("../common_lib")

sys.path.append("{}/../common_lib".format(os.path.abspath(__file__).
                                          replace(os.path.basename(__file__), "")))

sys.path.append("{}/../User_lib".format(os.path.abspath(__file__).
                                          replace(os.path.basename(__file__), "")))


from lib_myPrint import MyPrint
from MyImages import MyImages

from  Test import *


# define class
myPrint = MyPrint()
myPrint.debug("test print")


version = '1.0'


class MainFrame(wx.Frame):

    images = MyImages()
    default_with = 1000
    default_height = 700

    def __init__(self, parent, title='Default GUI', test_list=[]):
        # super(MainFrame, self).__init__(parent,
        #                                 title=title,
        #                                 size=(self.default_with, self.default_height))

        wx.Frame.__init__(self, None, title=title, size=(self.default_with, self.default_height))

        # define
        self.ListControlHeader = ["Test Name", "Status"]
        self.item_index = 0
        self.test_list = test_list

        self.testThread = None
        self.isPause = False

        # set icon for application
        try:
            icon = wx.Icon()
            data = self.images.getIconApp()
            bytes_stream = io.BytesIO(data)
            image = wx.Image(bytes_stream)
            icon.CopyFromBitmap(wx.Bitmap(image))
            self.SetIcon(icon)
        except Exception as e:
            myPrint.error(e)
            pass
        # self.SetBackgroundColour('blue')
        # set minimum size
        # self.SetSizeHints(wx.Size(600, 350), wx.DefaultSize)
        self.menu_bar_init()
        self.tool_bar_init()
        self.main_panel_init()
        self.statusBar = self.CreateStatusBar(1)

        # TODO: add exist event to handle if app still in thread

        self.Centre()
        # self.Show()
        self.Layout()

    def menu_bar_init(self):

        # list menu
        menubar = wx.MenuBar()
        filem = wx.Menu()
        editm = wx.Menu()
        optionm = wx.Menu()
        windowm = wx.Menu()

        # list menu in file
        itemNew = wx.MenuItem(filem, wx.ID_ANY, "New", wx.EmptyString, wx.ITEM_NORMAL)
        itemOpen = wx.MenuItem(filem, wx.ID_ANY, "Open", wx.EmptyString, wx.ITEM_NORMAL)
        itemSave = wx.MenuItem(filem, wx.ID_ANY, "Save", wx.EmptyString, wx.ITEM_NORMAL)
        itemSaveAs = wx.MenuItem(filem, wx.ID_ANY, "Save As...", wx.EmptyString, wx.ITEM_NORMAL)
        itemQuit = wx.MenuItem(filem, wx.ID_ANY, "Quit", wx.EmptyString, wx.ITEM_NORMAL)
        filem.Append(itemNew)
        filem.Append(itemOpen)
        filem.AppendSeparator()
        filem.Append(itemSave)
        filem.Append(itemSaveAs)
        filem.AppendSeparator()
        filem.Append(itemQuit)

        # list menu in edit
        itemUndo = wx.MenuItem(editm, wx.ID_ANY, "Undo", wx.EmptyString, wx.ITEM_NORMAL)
        itemRedo = wx.MenuItem(editm, wx.ID_ANY, "Redo", wx.EmptyString, wx.ITEM_NORMAL)
        itemCut = wx.MenuItem(editm, wx.ID_ANY, "Cut", wx.EmptyString, wx.ITEM_NORMAL)
        itemCopy = wx.MenuItem(editm, wx.ID_ANY, "Copy", wx.EmptyString, wx.ITEM_NORMAL)
        itemPaste = wx.MenuItem(editm, wx.ID_ANY, "Paste", wx.EmptyString, wx.ITEM_NORMAL)
        itemDelete = wx.MenuItem(editm, wx.ID_ANY, "Delete", wx.EmptyString, wx.ITEM_NORMAL)
        itemSelectAll = wx.MenuItem(editm, wx.ID_ANY, "Select All", wx.EmptyString, wx.ITEM_NORMAL)
        editm.Append(itemUndo)
        editm.Append(itemRedo)
        editm.AppendSeparator()
        editm.Append(itemCut)
        editm.Append(itemCopy)
        editm.Append(itemPaste)
        editm.Append(itemDelete)
        editm.Append(itemSelectAll)

        # list all menu in options
        itemMoreOptions = wx.MenuItem(optionm, wx.ID_ANY, "More Options", wx.EmptyString, wx.ITEM_NORMAL)
        itemHelp = wx.MenuItem(optionm, wx.ID_ANY, "Help", wx.EmptyString, wx.ITEM_NORMAL)
        optionm.Append(itemMoreOptions)
        optionm.Append(itemHelp)

        # list all menu in window
        itemWindows = wx.MenuItem(windowm, wx.ID_ANY, "Windows...", wx.EmptyString, wx.ITEM_NORMAL)
        windowm.Append(itemWindows)

        # show menu
        menubar.Append(filem, '&File')
        menubar.Append(editm, '&Edit')
        menubar.Append(optionm, '&Options')
        menubar.Append(windowm, '&Window')
        self.SetMenuBar(menubar)

        # bind events on the menu
        self.Bind(wx.EVT_MENU, self.on_new, itemNew)

        self.Bind(wx.EVT_MENU, self.on_quit, itemQuit)

    def tool_bar_init(self):
        self.id_stop = wx.NewId()
        self.id_pause = wx.NewId()
        self.id_play = wx.NewId()

        self.toolBar = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        iconSize = (24, 24)
        self.toolBar.SetToolBitmapSize(iconSize)

        # Icons "new" and "save"
        icon = self.images.getIconNew()
        icon_stream = io.BytesIO(icon)
        toolNew = self.toolBar.AddTool(wx.ID_ANY, "New",
                                  bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                  shortHelp="New")
        icon_stream.close()
        # self.toolBar.AddSeparator()
        icon = self.images.getIconSave()
        icon_stream = io.BytesIO(icon)
        toolSave = self.toolBar.AddTool(wx.ID_ANY, "Save",
                                   bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                   shortHelp="Save")
        icon_stream.close()

        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()

        # Icons "play", "pause" and "stop"
        icon = self.images.getIconPlay()
        icon_stream = io.BytesIO(icon)
        toolRun = self.toolBar.AddTool(self.id_play, "Run",
                                  bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                  shortHelp="Run")
        icon_stream.close()
        # self.toolBar.AddSeparator()
        icon = self.images.getIconPause()
        icon_stream = io.BytesIO(icon)
        toolPause = self.toolBar.AddTool(self.id_pause, "Pause",
                                  bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                  shortHelp="Pause")
        icon_stream.close()
        # self.toolBar.AddSeparator()
        icon = self.images.getIconStop()
        icon_stream = io.BytesIO(icon)
        toolStop = self.toolBar.AddTool(self.id_stop, "Stop",
                                   bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                   shortHelp="Stop")

        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()

        # Icons "clear", "help" and "quit"
        icon = self.images.getIconClear()
        icon_stream = io.BytesIO(icon)
        toolClear = self.toolBar.AddTool(wx.ID_ANY, "Save",
                                    bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                    shortHelp="Clear Logs")
        icon_stream.close()
        # self.toolBar.AddSeparator()
        icon = self.images.getIconHelp()
        icon_stream = io.BytesIO(icon)
        toolHelp = self.toolBar.AddTool(wx.ID_ANY, "Help",
                                   bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                   shortHelp="Help")
        icon_stream.close()
        # self.toolBar.AddSeparator()
        icon = self.images.getIconQuit()
        icon_stream = io.BytesIO(icon)
        toolQuit = self.toolBar.AddTool(wx.ID_ANY, "Quit",
                                   bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                   shortHelp="Quit")
        icon_stream.close()
        del icon, icon_stream

        self.toolBar.EnableTool(self.id_stop, False)
        self.toolBar.EnableTool(self.id_pause, False)
        self.toolBar.Realize()

        # bind events on the tools
        self.Bind(wx.EVT_TOOL, self.on_quit, toolQuit)
        self.Bind(wx.EVT_TOOL, self.on_save, toolSave)
        self.Bind(wx.EVT_TOOL, self.on_clear, toolClear)
        self.Bind(wx.EVT_TOOL, self.on_help, toolHelp)
        self.Bind(wx.EVT_TOOL, self.on_new, toolNew)

        self.Bind(wx.EVT_TOOL, self.on_run, toolRun)
        self.Bind(wx.EVT_TOOL, self.on_pause, toolPause)
        self.Bind(wx.EVT_TOOL, self.on_stop, toolStop)

    def main_panel_init(self):

        self.splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
    
        self.run_panel = wx.Panel(self.splitter)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticLine(self.run_panel), 0, wx.ALL | wx.EXPAND, 0)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.tCtrl1 = wx.TextCtrl(self.run_panel,
                                  size=(self.default_with/3*2, self.default_height),
                                  style=(wx.TE_MULTILINE | wx.TE_READONLY
                                         | wx.TE_RICH2 | wx.EXPAND))
        fgs = wx.FlexGridSizer(1, 1, 5, 5)
        fgs.Add(self.tCtrl1, 1, wx.EXPAND)
        fgs.AddGrowableCol(0, 0)
        hbox1.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=0)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2)
        vbox.Add((-1, 5))
        self.run_panel.SetSizer(vbox)


        self.list_panel = wx.Panel(self.splitter)
        vbox_list = wx.BoxSizer(wx.VERTICAL)
        vbox_list.Add(wx.StaticLine(self.list_panel), 0, wx.ALL | wx.EXPAND, 0)
        self.my_list_control = wx.ListCtrl(self.list_panel, size=(self.default_with/3, self.default_height),
                                           style=wx.LC_REPORT | wx.BORDER_SUNKEN
                                                 | wx.LC_HRULES | wx.LC_VRULES | wx.EXPAND)
        for i in range(len(self.ListControlHeader)):
            self.my_list_control.InsertColumn(i, self.ListControlHeader[i],
                                              width=self.default_with/3/2)
        # add default from main app
        for i in range(len(self.test_list)):
            self.list_control_add_new([self.test_list[i], "NO RUN"])
        fgs2 = wx.FlexGridSizer(1, 1, 5, 5)
        fgs2.Add(self.my_list_control, 1, wx.ALIGN_TOP | wx.EXPAND)
        fgs2.AddGrowableCol(0, 0)
        vbox_list.Add(fgs2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2)
        vbox_list.Add((-1, 5))
        self.list_panel.SetSizer(vbox_list)

        # Set splitter 
        self.splitter.SplitVertically(self.list_panel, self.run_panel, 320)
        self.splitter.SetMinimumPaneSize(200)

        # self.Bind(wx.EVT_BUTTON, self.btn1_event, self.btn1)
        # self.Bind(wx.EVT_BUTTON, self.btn2_event, self.btn2)
        # self.Bind(wx.EVT_BUTTON, self.btn3_event, self.btn3)


    def list_control_add_new(self, data):
        '''
        :param data: ["test_name", "result"]
        :return:
        '''
        # TODO: test here
        self.my_list_control.Append(data)
        if self.item_index % 2:
            self.my_list_control.SetItemBackgroundColour(self.item_index, "white")
        else:
            self.my_list_control.SetItemBackgroundColour(self.item_index, "gray")
        self.item_index += 1

    # --- Even ---
    def on_new(self, evt):
        # TODO: test
        self.list_control_add_new(["test_", "NO RUN"])

    def on_run(self, evt):
        # enable 'pause', 'stop'
        self.toolBar.EnableTool(self.id_play, False)
        self.toolBar.EnableTool(self.id_stop, True)
        self.toolBar.EnableTool(self.id_pause, True)
        # TODO: test Here
        if not self.isPause:
            self.testThread = Test(self.test_list, self.tCtrl1)
            self.testThread.start()
        else:
            self.isPause = False
            # resume
            safe_print("=======Resume test==============")
            self.testThread.Continue()

    def on_pause(self, evt):
        if self.testThread:
            self.isPause = True
            self.testThread.Pause()
            # time.sleep(0.5)
            safe_print("=======Pause test==============")
            self.toolBar.EnableTool(self.id_play, True)
            self.toolBar.EnableTool(self.id_pause, False)
            self.toolBar.EnableTool(self.id_stop, True)
        pass

    def on_stop(self, evt):
        if self.testThread:
            self.isPause = False
            self.testThread.stop()
            safe_print("=======Stoped test==============")
            self.toolBar.EnableTool(self.id_pause, False)
            self.toolBar.EnableTool(self.id_play, True)
            self.toolBar.EnableTool(self.id_stop, False)
        pass

    def on_save(self, evt):
        pass

    def on_clear(self, evt):
        # TODO: test
        self.my_list_control.DeleteAllItems()
        self.item_index = 0
        pass

    def on_help(self, evt):
        pass

    def on_quit(self, evt):
        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
                                wx.YES_NO | wx.ICON_EXCLAMATION)
        _response = dial.ShowModal()
        if _response == wx.ID_YES:
            self.Close(True)
        else:
            return 0

    def btn1_event(self, evt):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()

    def btn2_event(self, evt):
        pass

    def btn3_event(self, evt):
        pass


if __name__ == '__main__':
    app = wx.App()
    main_frame = MainFrame(None, test_list=["test_script.py"])
    # main_frame = MainFrame(None, test_list=["MainFrame\\test_script.py"])
    main_frame.Show()
    app.MainLoop()
